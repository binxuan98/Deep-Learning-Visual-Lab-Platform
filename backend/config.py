import os


class Config:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATABASE_PATH = os.path.join(BASE_DIR, "data", "platform.db")
    UPLOAD_IMAGE_DIR = os.path.join(BASE_DIR, "uploads", "images")
    UPLOAD_VIDEO_DIR = os.path.join(BASE_DIR, "uploads", "videos")
    OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
    LOG_FILE_PATH = os.path.join(BASE_DIR, "data", "system.log")
    SECRET_KEY = "deep-learning-visual-lab-secret"
    ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp"}
    ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024
