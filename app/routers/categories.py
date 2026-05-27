from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryResponse, status_code=201)
async def create_category(data: CategoryCreate, session: AsyncSession = Depends(get_db_session)):
    service = CategoryService(session)
    return await service.create_category(data)


@router.get("", response_model=List[CategoryResponse])
async def list_categories(
    printable_only: bool = Query(False),
    session: AsyncSession = Depends(get_db_session),
):
    service = CategoryService(session)
    return await service.list_categories(printable_only=printable_only)


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CategoryService(session)
    return await service.get_category(category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int, data: CategoryUpdate, session: AsyncSession = Depends(get_db_session)
):
    service = CategoryService(session)
    return await service.update_category(category_id, data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CategoryService(session)
    await service.delete_category(category_id)
