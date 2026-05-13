import uvicorn

from home.core.config import settings


def main() -> None:
    uvicorn.run("home.app:app", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
