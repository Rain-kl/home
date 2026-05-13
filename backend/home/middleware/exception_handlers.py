from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger

from home.schemas.result_schema import error
from home.services.auth_service import AuthError


def _json_result(code: int, msg: str, status_code: int = 200) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=error(msg=msg, code=code).model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning("参数验证失败: {} {}", request.url.path, exc.errors())
        messages = [str(item.get("msg", "参数验证失败")) for item in exc.errors()]
        return _json_result(400, "; ".join(messages) or "参数验证失败")

    @app.exception_handler(AuthError)
    async def auth_exception_handler(request: Request, exc: AuthError):
        logger.warning("登录异常: {} {}", request.url.path, exc)
        return _json_result(401, str(exc))

    @app.exception_handler(Exception)
    async def system_exception_handler(request: Request, exc: Exception):
        logger.exception("系统异常: {}", request.url.path)
        return _json_result(500, "系统异常，请稍后重试")
