import logging
import sys
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.database import engine
from app.errors import (
    AppException,
    app_exception_handler,
    generic_exception_handler,
    integrity_error_handler,
    validation_exception_handler,
)
from app.middleware.auth import get_current_user
from app.middleware.correlation_id import CorrelationIDMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.routers import (
    auth, card_layouts, categories, certificates, custom_fields,
    dinner, display, events, files, hall, kit, lunch, notifications,
    registrations, reports, search,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    from app.models.base import Base
    import app.models  # noqa: F401 — ensure all models loaded
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def setup_logging() -> None:
    if settings.LOG_FORMAT == "json":
        formatter = logging.Formatter(
            '{"timestamp":"%(asctime)s","level":"%(levelname)s","request_id":"%(request_id)s",'
            '"message":"%(message)s"}'
        )
    else:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(request_id)s] %(message)s"
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    root_logger.handlers.clear()
    root_logger.addHandler(handler)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="Registration System API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        max_age=600,
    )

    app.add_middleware(CorrelationIDMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitMiddleware, max_attempts=5, window_seconds=900)

    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    _auth = Depends(get_current_user)

    app.include_router(auth.router, prefix="/api/v1", dependencies=[])
    app.include_router(events.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(categories.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(registrations.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(custom_fields.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(card_layouts.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(search.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(kit.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(lunch.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(dinner.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(hall.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(certificates.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(reports.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(notifications.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(display.router, prefix="/api/v1", dependencies=[_auth])
    app.include_router(files.router, prefix="/api/v1", dependencies=[_auth])

    return app


app = create_app()
