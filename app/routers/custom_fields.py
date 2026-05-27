from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.custom_field import CustomFieldCreate, CustomFieldResponse, CustomFieldUpdate, FieldOrderUpdate
from app.services.custom_field_service import CustomFieldService

router = APIRouter(prefix="/custom-fields", tags=["custom_fields"])


@router.post("", response_model=CustomFieldResponse, status_code=201)
async def create_field(data: CustomFieldCreate, session: AsyncSession = Depends(get_db_session)):
    service = CustomFieldService(session)
    return await service.add_field(data)


@router.get("/event/{event_id}", response_model=List[CustomFieldResponse])
async def list_fields(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CustomFieldService(session)
    return await service.list_fields(event_id)


@router.put("/{field_id}", response_model=CustomFieldResponse)
async def update_field(
    field_id: int, data: CustomFieldUpdate, session: AsyncSession = Depends(get_db_session)
):
    service = CustomFieldService(session)
    return await service.update_field(field_id, data)


@router.delete("/{field_id}", status_code=204)
async def delete_field(field_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CustomFieldService(session)
    await service.remove_field(field_id)


@router.put("/reorder", response_model=List[CustomFieldResponse])
async def reorder_fields(orders: List[FieldOrderUpdate], session: AsyncSession = Depends(get_db_session)):
    service = CustomFieldService(session)
    return await service.reorder_fields(orders)
