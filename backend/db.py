import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Optional


def ensure_parent_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def get_connection(database_path: str) -> sqlite3.Connection:
    ensure_parent_dir(database_path)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


@contextmanager
def db_cursor(database_path: str):
    connection = get_connection(database_path)
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    finally:
        connection.close()


def init_db(database_path: str) -> None:
    with db_cursor(database_path) as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                input_path TEXT NOT NULL,
                output_path TEXT NOT NULL,
                result_text TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            INSERT OR IGNORE INTO users (username, password, role, created_at)
            VALUES (?, ?, ?, ?)
            """,
            ("admin", "admin123", "teacher", datetime.now().isoformat()),
        )


def insert_log(database_path: str, level: str, message: str) -> None:
    with db_cursor(database_path) as cursor:
        cursor.execute(
            "INSERT INTO logs (level, message, created_at) VALUES (?, ?, ?)",
            (level, message, datetime.now().isoformat()),
        )


def insert_history(
    database_path: str,
    username: str,
    algorithm: str,
    input_path: str,
    output_path: str,
    result_text: str,
) -> None:
    with db_cursor(database_path) as cursor:
        cursor.execute(
            """
            INSERT INTO history (username, algorithm, input_path, output_path, result_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (username, algorithm, input_path, output_path, result_text, datetime.now().isoformat()),
        )


def query_history(database_path: str, username: Optional[str] = None):
    with db_cursor(database_path) as cursor:
        if username:
            cursor.execute(
                "SELECT * FROM history WHERE username = ? ORDER BY id DESC LIMIT 200",
                (username,),
            )
        else:
            cursor.execute("SELECT * FROM history ORDER BY id DESC LIMIT 200")
        return [dict(row) for row in cursor.fetchall()]


def query_logs(database_path: str):
    with db_cursor(database_path) as cursor:
        cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 200")
        return [dict(row) for row in cursor.fetchall()]


def query_user(database_path: str, username: str, password: str):
    with db_cursor(database_path) as cursor:
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ? LIMIT 1",
            (username, password),
        )
        row = cursor.fetchone()
        return dict(row) if row else None
