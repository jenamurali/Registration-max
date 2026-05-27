from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.registration import RegistrationCounts, RegistrationCreate, RegistrationResponse, RegistrationUpdate
from app.services.registration_service import RegistrationService

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.post("", response_model=RegistrationResponse, status_code=201)
async def create_registration(data: RegistrationCreate, session: AsyncSession = Depends(get_db_session)):
    service = RegistrationService(session)
    return await service.register(data)


@router.get("", response_model=List[RegistrationResponse])
async def search_registrations(
    name: str | None = Query(None),
    company_name: str | None = Query(None),
    email: str | None = Query(None),
    mobile: str | None = Query(None),
    city: str | None = Query(None),
    country: str | None = Query(None),
    event_id: int | None = Query(None),
    session: AsyncSession = Depends(get_db_session),
):
    service = RegistrationService(session)
    from app.repositories.registration_repo import RegistrationRepository
    repo = RegistrationRepository(session)
    results = await repo.search(
        name=name, company_name=company_name, email=email,
        mobile=mobile, city=city, country=country, event_id=event_id,
    )
    return results


@router.get("/counts/{event_id}", response_model=RegistrationCounts)
async def get_counts(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = RegistrationService(session)
    return await service.get_counts(event_id)


@router.get("/barcode/{barcode}", response_model=RegistrationResponse)
async def get_by_barcode(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = RegistrationService(session)
    return await service.get_by_barcode(barcode)


@router.get("/{reg_id}", response_model=RegistrationResponse)
async def get_registration(reg_id: int, session: AsyncSession = Depends(get_db_session)):
    service = RegistrationService(session)
    return await service.get_registration(reg_id)


@router.put("/{reg_id}", response_model=RegistrationResponse)
async def update_registration(
    reg_id: int, data: RegistrationUpdate, session: AsyncSession = Depends(get_db_session)
):
    service = RegistrationService(session)
    return await service.update_registration(reg_id, data)


@router.delete("/{reg_id}", status_code=204)
async def delete_registration(reg_id: int, session: AsyncSession = Depends(get_db_session)):
    service = RegistrationService(session)
    await service.delete_registration(reg_id)


@router.post("/{reg_id}/print", response_model=RegistrationResponse)
async def record_print(reg_id: int, session: AsyncSession = Depends(get_db_session)):
    service = RegistrationService(session)
    return await service.increment_print_count(reg_id)
