import os
import uuid
from typing import Set
from werkzeug.datastructures import FileStorage


def save_upload_file(file: FileStorage, target_dir: str) -> str:
    os.makedirs(target_dir, exist_ok=True)
    extension = os.path.splitext(file.filename or "")[1].lower()
    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = os.path.join(target_dir, filename)
    file.save(file_path)
    return file_path


def extension_allowed(filename: str, allowed_extensions: Set[str]) -> bool:
    extension = os.path.splitext(filename)[1].lower()
    return extension in allowed_extensions
