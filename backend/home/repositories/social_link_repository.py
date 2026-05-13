from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from home.models.social_link import CmsSocialLink
from home.schemas.social_link_schema import SocialLinkInput


class SocialLinkRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_enabled(self) -> list[CmsSocialLink]:
        stmt = (
            select(CmsSocialLink)
            .where(CmsSocialLink.enabled_flag == 1)
            .order_by(CmsSocialLink.sort_order.asc(), CmsSocialLink.id.asc())
        )
        return list(self.db.scalars(stmt).all())

    def list_all(self) -> list[CmsSocialLink]:
        stmt = select(CmsSocialLink).order_by(
            CmsSocialLink.sort_order.asc(), CmsSocialLink.id.asc()
        )
        return list(self.db.scalars(stmt).all())

    def replace_all(self, input_list: list[SocialLinkInput]) -> bool:
        self.db.execute(delete(CmsSocialLink))
        for index, item in enumerate(input_list, start=1):
            self.db.add(
                CmsSocialLink(
                    name=item.name,
                    icon=item.icon,
                    tip=item.tip,
                    url=item.url,
                    sort_order=item.sort_order if item.sort_order is not None else index,
                    enabled_flag=item.enabled_flag if item.enabled_flag is not None else 1,
                )
            )
        self.db.commit()
        return True
