import os
import uuid

from fastapi import UploadFile, HTTPException

from app.utils.constants import UPLOAD_DIR, ALLOWED_IMAGE_EXTENSIONS, MAX_IMAGE_SIZE_MB


def save_upload_file(file: UploadFile, subdirectory: str = "") -> str:
    """Save an uploaded image file to disk and return its relative path."""
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"File type {ext} not allowed")

    target_dir = os.path.join(UPLOAD_DIR, subdirectory)
    os.makedirs(target_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(target_dir, filename)

    contents = file.file.read()
    if len(contents) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large (max {MAX_IMAGE_SIZE_MB}MB)")

    with open(filepath, "wb") as f:
        f.write(contents)

    return filepath