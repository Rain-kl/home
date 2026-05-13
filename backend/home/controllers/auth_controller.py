from fastapi import APIRouter, Cookie, Depends, Form, Response

from home.controllers.dependencies import require_login
from home.core.config import settings
from home.schemas.auth_schema import AdminInfo
from home.schemas.result_schema import Result, success
from home.services.auth_service import auth_service

router = APIRouter(prefix="/oms/auth", tags=["auth"])


@router.post("/login", response_model=Result[bool])
def login(response: Response, username: str = Form(), password: str = Form()):
    token = auth_service.login(username, password)
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        samesite="lax",
    )
    return success(True)


@router.get("/info", response_model=Result[AdminInfo], dependencies=[Depends(require_login)])
def info():
    return success(AdminInfo(username=settings.admin_username, nickname="管理员"))


@router.post("/logout", response_model=Result[bool])
def logout(
    response: Response,
    token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
):
    auth_service.logout(token)
    response.delete_cookie(settings.session_cookie_name)
    return success(True)
