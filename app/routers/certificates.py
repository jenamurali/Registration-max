from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.certificate import CertificateData, CertificateTemplateResponse, TemplateConfig
from app.services.certificate_service import CertificateService

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.get("/scan", response_model=CertificateData)
async def get_by_scan(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = CertificateService(session)
    return await service.get_certificate_data(barcode)


@router.get("/search", response_model=List[CertificateData])
async def search_certificates(query: str = Query(...), session: AsyncSession = Depends(get_db_session)):
    service = CertificateService(session)
    return await service.search_certificate_data(query)


@router.get("/template/{event_id}", response_model=CertificateTemplateResponse)
async def get_template(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CertificateService(session)
    return await service.get_template(event_id)


@router.put("/template/{event_id}", response_model=CertificateTemplateResponse)
async def save_template(
    event_id: int, data: TemplateConfig, session: AsyncSession = Depends(get_db_session)
):
    service = CertificateService(session)
    return await service.save_template(event_id, data.template_config)
