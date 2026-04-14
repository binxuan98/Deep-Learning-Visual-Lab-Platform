import os
from datetime import datetime

from backend.db import insert_log


def app_log(database_path: str, log_file_path: str, level: str, message: str) -> None:
    insert_log(database_path, level, message)
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    with open(log_file_path, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now().isoformat()} [{level}] {message}\n")
