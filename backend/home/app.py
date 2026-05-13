from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from home.controllers import auth_controller, site_link_controller
from home.core.config import settings
from home.core.database import init_db
from home.middleware.exception_handlers import register_exception_handlers
from home.middleware.logging import RequestLoggingMiddleware, configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count"],
    )
    register_exception_handlers(app)

    app.include_router(auth_controller.router)
    app.include_router(site_link_controller.router)
    app.include_router(auth_controller.router, prefix="/api", include_in_schema=False)
    app.include_router(site_link_controller.router, prefix="/api", include_in_schema=False)

    static_dir = Path(__file__).resolve().parents[1] / "static"
    index_file = static_dir / "index.html"
    if index_file.exists():
        @app.get("/", include_in_schema=False)
        async def serve_index():
            return FileResponse(index_file)

        @app.get("/{path:path}", include_in_schema=False)
        async def serve_frontend(path: str):
            requested_file = (static_dir / path).resolve()
            if requested_file.is_file() and requested_file.is_relative_to(static_dir):
                return FileResponse(requested_file)
            return FileResponse(index_file)

    return app


app = create_app()
