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
    from home.models.social_link import CmsSocialLink
    from home.models.site_config import CmsSiteConfig
    from home.models.site_link import CmsSiteLink
    from home.repositories.site_config_repository import SiteConfigRepository

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
        if db.query(CmsSocialLink).first() is None:
            db.add_all(
                [
                    CmsSocialLink(
                        name="Github",
                        icon="/images/icon/github.png",
                        tip="去 Github 看看",
                        url="https://github.com/imsyy",
                        sort_order=1,
                    ),
                    CmsSocialLink(
                        name="BiliBili",
                        icon="/images/icon/bilibili.png",
                        tip="(゜-゜)つロ 干杯 ~",
                        url="https://space.bilibili.com/98544142",
                        sort_order=2,
                    ),
                    CmsSocialLink(
                        name="QQ",
                        icon="/images/icon/qq.png",
                        tip="有什么事吗",
                        url="https://res.abeim.cn/api/qq/?qq=1539250352",
                        sort_order=3,
                    ),
                    CmsSocialLink(
                        name="Email",
                        icon="/images/icon/email.png",
                        tip="来封 Email ~",
                        url="mailto:one@imsyy.top",
                        sort_order=4,
                    ),
                    CmsSocialLink(
                        name="Twitter",
                        icon="/images/icon/twitter.png",
                        tip="你懂的 ~",
                        url="https://twitter.com/iimmsyy",
                        sort_order=5,
                    ),
                    CmsSocialLink(
                        name="Telegram",
                        icon="/images/icon/telegram.png",
                        tip="你懂的 ~",
                        url="https://t.me/bottom_user",
                        sort_order=6,
                    ),
                ]
            )
            db.commit()
        if db.query(CmsSiteConfig).first() is None:
            SiteConfigRepository(db).ensure_defaults()
