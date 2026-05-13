from datetime import datetime, timedelta, timezone
from secrets import compare_digest, token_urlsafe

from home.core.config import settings


class AuthError(Exception):
    pass


class AuthService:
    def __init__(self) -> None:
        self._sessions: dict[str, datetime] = {}

    def login(self, username: str, password: str) -> str:
        if not (
            compare_digest(username, settings.admin_username)
            and compare_digest(password, settings.admin_password)
        ):
            raise AuthError("用户名或密码错误")
        token = token_urlsafe(32)
        self._sessions[token] = self._expires_at()
        return token

    def logout(self, token: str | None) -> None:
        if token:
            self._sessions.pop(token, None)

    def check_login(self, token: str | None) -> None:
        if not token:
            raise AuthError("未能读取到有效 token")
        expires_at = self._sessions.get(token)
        if expires_at is None:
            raise AuthError("token 无效")
        if expires_at < datetime.now(timezone.utc):
            self._sessions.pop(token, None)
            raise AuthError("token 已过期")

    def _expires_at(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(seconds=settings.session_ttl_seconds)


auth_service = AuthService()
