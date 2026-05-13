from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from home.models.site_link import CmsSiteLink
from home.schemas.site_link_schema import SiteLinkInput


class SiteLinkRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_enabled(self) -> list[CmsSiteLink]:
        stmt = (
            select(CmsSiteLink)
            .where(CmsSiteLink.enabled_flag == 1)
            .order_by(CmsSiteLink.sort_order.asc(), CmsSiteLink.id.asc())
        )
        return list(self.db.scalars(stmt).all())

    def list_all(self) -> list[CmsSiteLink]:
        stmt = select(CmsSiteLink).order_by(CmsSiteLink.sort_order.asc(), CmsSiteLink.id.asc())
        return list(self.db.scalars(stmt).all())

    def replace_all(self, input_list: list[SiteLinkInput]) -> bool:
        self.db.execute(delete(CmsSiteLink))
        for index, item in enumerate(input_list, start=1):
            self.db.add(
                CmsSiteLink(
                    icon=item.icon,
                    name=item.name,
                    link=item.link,
                    sort_order=item.sort_order if item.sort_order is not None else index,
                    enabled_flag=item.enabled_flag if item.enabled_flag is not None else 1,
                )
            )
        self.db.commit()
        return True
