from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.deps import get_auth_service
from app.errors import ForbiddenException
from app.services.auth_service import AuthService

bearer_scheme = HTTPBearer()


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await auth_service.get_current_user(credentials.credentials)
    request.state.user_id = user.id
    request.state.user_role = user.role
    return user


def require_admin(request: Request):
    role = getattr(request.state, "user_role", None)
    if role != "admin":
        raise ForbiddenException("Admin access required")
