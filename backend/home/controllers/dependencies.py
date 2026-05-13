from fastapi import Cookie, Depends
from sqlalchemy.orm import Session

from home.core.config import settings
from home.core.database import get_db
from home.repositories.site_link_repository import SiteLinkRepository
from home.services.auth_service import auth_service
from home.services.site_link_service import SiteLinkService
from home.utils.cache import TimedCache

public_cache = TimedCache(settings.public_cache_ttl_seconds)


def get_site_link_service(db: Session = Depends(get_db)) -> SiteLinkService:
    return SiteLinkService(SiteLinkRepository(db), public_cache)


def require_login(
    token: str | None = Cookie(default=None, alias=settings.session_cookie_name)
) -> None:
    auth_service.check_login(token)
