from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(data: UserCreate, session: AsyncSession = Depends(get_db_session)):
    auth_service = AuthService(session)
    return await auth_service.create_user(data.username, data.email, data.password, data.role)


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, session: AsyncSession = Depends(get_db_session)):
    auth_service = AuthService(session)
    return await auth_service.authenticate(request.username, request.password)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest, session: AsyncSession = Depends(get_db_session)):
    auth_service = AuthService(session)
    return await auth_service.refresh_token(request.refresh_token)
