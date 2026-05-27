import os
import uuid

from fastapi import UploadFile

from app.config import settings
from app.errors import ValidationException

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp"}
MAX_FILE_SIZE = 5 * 1024 * 1024


class FileStorageService:
    def __init__(self, upload_dir: str = "uploads"):
        self._upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    async def upload_photo(self, file: UploadFile) -> str:
        return await self._upload(file, "photos")

    async def upload_logo(self, file: UploadFile) -> str:
        return await self._upload(file, "logos")

    async def _upload(self, file: UploadFile, subdir: str) -> str:
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationException(f"File type '{ext}' not allowed")
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise ValidationException("File too large (max 5MB)")
        target_dir = os.path.join(self._upload_dir, subdir)
        os.makedirs(target_dir, exist_ok=True)
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(target_dir, filename)
        with open(filepath, "wb") as f:
            f.write(contents)
        return filepath

    def get_file_path(self, filepath: str) -> str:
        return filepath

    def delete_file(self, filepath: str) -> None:
        if os.path.exists(filepath):
            os.remove(filepath)
