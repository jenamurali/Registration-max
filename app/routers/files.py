from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.services.file_storage_service import FileStorageService

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload/photo")
async def upload_photo(file: UploadFile, session: AsyncSession = Depends(get_db_session)):
    service = FileStorageService()
    filepath = await service.upload_photo(file)
    return {"filepath": filepath}


@router.post("/upload/logo")
async def upload_logo(file: UploadFile, session: AsyncSession = Depends(get_db_session)):
    service = FileStorageService()
    filepath = await service.upload_logo(file)
    return {"filepath": filepath}
