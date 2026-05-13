from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from home.core.database import Base


class CmsSiteLink(Base):
    __tablename__ = "cms_site_link"
    __table_args__ = (
        Index("idx_sort_order", "sort_order"),
        Index("idx_enabled_flag", "enabled_flag"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    icon: Mapped[str | None] = mapped_column(String(64))
    name: Mapped[str | None] = mapped_column(String(64))
    link: Mapped[str | None] = mapped_column(String(500))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    enabled_flag: Mapped[int] = mapped_column(Integer, default=1)
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
