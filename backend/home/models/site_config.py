from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from home.core.database import Base


class CmsSiteConfig(Base):
    __tablename__ = "cms_site_config"
    __table_args__ = (
        UniqueConstraint("config_key", name="uk_config_key"),
        Index("idx_config_group", "config_group"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    config_key: Mapped[str] = mapped_column(String(64), nullable=False)
    config_value: Mapped[str | None] = mapped_column(Text)
    config_group: Mapped[str] = mapped_column(String(32), default="site")
    label: Mapped[str | None] = mapped_column(String(64))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
