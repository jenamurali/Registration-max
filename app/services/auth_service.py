from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.errors import AuthException, ConflictException, ForbiddenException
from app.models.user import User
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, session: AsyncSession):
        self._user_repo = UserRepository(session)

    async def create_user(self, username: str, email: str, password: str, role: str = "operator") -> User:
        existing = await self._user_repo.get_by_username(username)
        if existing:
            raise ConflictException("Username already exists")
        existing = await self._user_repo.get_by_email(email)
        if existing:
            raise ConflictException("Email already exists")
        user = User(
            username=username,
            email=email,
            password_hash=self._hash_password(password),
            role=role,
        )
        return await self._user_repo.add(user)

    async def authenticate(self, username: str, password: str) -> dict:
        user = await self._user_repo.get_by_username(username)
        if not user:
            raise AuthException("Invalid username or password")
        if not self._verify_password(password, user.password_hash):
            raise AuthException("Invalid username or password")
        if not user.is_active:
            raise ForbiddenException("Account is deactivated")
        access_token = self._create_access_token(user.id, user.role)
        refresh_token = self._create_refresh_token(user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        payload = self._decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthException("Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise AuthException("Invalid token")
        user = await self._user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise AuthException("User not found or inactive")
        access_token = self._create_access_token(user.id, user.role)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def get_current_user(self, token: str) -> User:
        payload = self._decode_token(token)
        if payload.get("type") != "access":
            raise AuthException("Invalid token type")
        user_id = payload.get("sub")
        if not user_id:
            raise AuthException("Invalid token")
        user = await self._user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise AuthException("User not found or inactive")
        return user

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

    def _create_access_token(self, user_id: int, role: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "role": role,
            "type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def _create_refresh_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def _decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except JWTError:
            raise AuthException("Invalid or expired token")
