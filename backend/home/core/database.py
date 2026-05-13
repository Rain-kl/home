from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from home.core.config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

if settings.database_url.startswith("sqlite:///./"):
    db_path = Path(settings.database_url.removeprefix("sqlite:///"))
    db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from home.models.site_link import CmsSiteLink

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(CmsSiteLink).first() is None:
            db.add_all(
                [
                    CmsSiteLink(
                        icon="Blog", name="博客", link="https://blog.imsyy.top/", sort_order=1
                    ),
                    CmsSiteLink(
                        icon="Cloud", name="网盘", link="https://pan.imsyy.top/", sort_order=2
                    ),
                    CmsSiteLink(
                        icon="CompactDisc",
                        name="音乐",
                        link="https://music.imsyy.top/",
                        sort_order=3,
                    ),
                    CmsSiteLink(
                        icon="Compass", name="起始页", link="https://nav.imsyy.top/", sort_order=4
                    ),
                    CmsSiteLink(
                        icon="Book", name="网址集", link="https://web.imsyy.top/", sort_order=5
                    ),
                    CmsSiteLink(
                        icon="Fire", name="今日热榜", link="https://hot.imsyy.top/", sort_order=6
                    ),
                    CmsSiteLink(
                        icon="LaptopCode",
                        name="站点监测",
                        link="https://status.imsyy.top/",
                        sort_order=7,
                    ),
                ]
            )
            db.commit()
