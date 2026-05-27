import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_attempts: int = 5, window_seconds: int = 900):
        super().__init__(app)
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/api/v1/auth/login" and request.method == "POST":
            body = await request.body()
            try:
                import json
                username = json.loads(body).get("username", "")
            except Exception:
                username = ""
            request._body = body

            if username and self._is_rate_limited(username):
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Too many login attempts. Try again later."},
                )

            response = await call_next(request)

            if username and response.status_code == 401:
                self._record_attempt(username)

            return response

        return await call_next(request)

    def _is_rate_limited(self, username: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        self._attempts[username] = [t for t in self._attempts[username] if t > cutoff]
        return len(self._attempts[username]) >= self.max_attempts

    def _record_attempt(self, username: str) -> None:
        self._attempts[username].append(time.time())
