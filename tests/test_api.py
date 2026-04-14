import io
import os
import sys
import tempfile

import numpy as np
from PIL import Image

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import app
from backend.db import init_db


def _create_image_bytes():
    image = Image.fromarray(np.zeros((64, 64, 3), dtype=np.uint8))
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    stream.seek(0)
    return stream


def test_login_and_algorithms():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "platform.db")
        init_db(db_path)
        app.config.update(
            TESTING=True,
            DATABASE_PATH=db_path,
            UPLOAD_IMAGE_DIR=os.path.join(tmpdir, "images"),
            UPLOAD_VIDEO_DIR=os.path.join(tmpdir, "videos"),
            OUTPUT_DIR=os.path.join(tmpdir, "outputs"),
            LOG_FILE_PATH=os.path.join(tmpdir, "system.log"),
        )
        os.makedirs(app.config["UPLOAD_IMAGE_DIR"], exist_ok=True)
        os.makedirs(app.config["UPLOAD_VIDEO_DIR"], exist_ok=True)
        os.makedirs(app.config["OUTPUT_DIR"], exist_ok=True)

        with app.test_client() as client:
            login_resp = client.post("/api/login", json={"username": "admin", "password": "admin123"})
            assert login_resp.status_code == 200

            algo_resp = client.get("/api/algorithms")
            assert algo_resp.status_code == 200
            assert len(algo_resp.json["algorithms"]) >= 6


def test_upload_and_run_yolo():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "platform.db")
        init_db(db_path)
        app.config.update(
            TESTING=True,
            DATABASE_PATH=db_path,
            UPLOAD_IMAGE_DIR=os.path.join(tmpdir, "images"),
            UPLOAD_VIDEO_DIR=os.path.join(tmpdir, "videos"),
            OUTPUT_DIR=os.path.join(tmpdir, "outputs"),
            LOG_FILE_PATH=os.path.join(tmpdir, "system.log"),
        )
        os.makedirs(app.config["UPLOAD_IMAGE_DIR"], exist_ok=True)
        os.makedirs(app.config["UPLOAD_VIDEO_DIR"], exist_ok=True)
        os.makedirs(app.config["OUTPUT_DIR"], exist_ok=True)

        with app.test_client() as client:
            client.post("/api/login", json={"username": "admin", "password": "admin123"})
            file_stream = _create_image_bytes()
            upload_resp = client.post(
                "/api/upload/image",
                data={"file": (file_stream, "demo.png")},
                content_type="multipart/form-data",
            )
            assert upload_resp.status_code == 200
            file_path = upload_resp.json["file_path"]

            run_resp = client.post("/api/run/yolo", json={"file_path": file_path})
            assert run_resp.status_code == 200
            assert run_resp.json["success"] is True
