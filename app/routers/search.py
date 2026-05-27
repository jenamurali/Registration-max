from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.registration import RegistrationResponse
from app.repositories.registration_repo import RegistrationRepository

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=List[RegistrationResponse])
async def search(
    name: str | None = Query(None),
    company_name: str | None = Query(None),
    email: str | None = Query(None),
    mobile: str | None = Query(None),
    city: str | None = Query(None),
    country: str | None = Query(None),
    event_id: int | None = Query(None),
    session: AsyncSession = Depends(get_db_session),
):
    repo = RegistrationRepository(session)
    return await repo.search(
        name=name, company_name=company_name, email=email,
        mobile=mobile, city=city, country=country, event_id=event_id,
    )
