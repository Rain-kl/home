from sqlalchemy import select
from sqlalchemy.orm import Session

from home.models.site_config import CmsSiteConfig


DEFAULT_SITE_CONFIGS = [
    ("siteName", "主页", "site", "站点名称"),
    ("siteAuthor", "Ryan", "site", "站点作者"),
    ("siteKeywords", "个人主页", "site", "关键词"),
    ("siteDescription", "一个默默无闻的主页", "site", "站点简介"),
    ("siteUrl", "Arctel.net", "site", "站点地址"),
    ("siteLogo", "/images/icon/favicon.ico", "site", "浏览器图标"),
    ("siteMainLogo", "/images/icon/logo.png", "site", "主页头像"),
    ("siteAppleLogo", "/images/logo/apple-touch-icon.png", "site", "Apple 图标"),
    ("descHello", "Hello World !", "description", "默认招呼"),
    ("descText", "一个建立于 21 世纪的小站，存活于互联网的边缘", "description", "默认简介"),
    ("descHelloOther", "Oops !", "description", "切换招呼"),
    ("descTextOther", "哎呀，这都被你发现了（ 再点击一次可关闭 ）", "description", "切换简介"),
    ("weatherKey", "", "weather", "高德天气 Key"),
    ("siteStart", "2020-10-24", "site", "建站日期"),
    ("siteIcp", "", "site", "ICP备案号"),
]


class SiteConfigRepository:
    def __init__(self, db: Session):
        self.db = db

    def ensure_defaults(self) -> None:
        existing_keys = set(self.db.scalars(select(CmsSiteConfig.config_key)).all())
        for index, (key, value, group, label) in enumerate(DEFAULT_SITE_CONFIGS, start=1):
            if key not in existing_keys:
                self.db.add(
                    CmsSiteConfig(
                        config_key=key,
                        config_value=value,
                        config_group=group,
                        label=label,
                        sort_order=index,
                    )
                )
        self.db.commit()

    def list_all(self) -> list[CmsSiteConfig]:
        stmt = select(CmsSiteConfig).order_by(
            CmsSiteConfig.config_group.asc(),
            CmsSiteConfig.sort_order.asc(),
            CmsSiteConfig.id.asc(),
        )
        return list(self.db.scalars(stmt).all())

    def get_public_map(self) -> dict[str, str | None]:
        return {item.config_key: item.config_value for item in self.list_all()}

    def save_map(self, configs: dict[str, str | None]) -> bool:
        known_defaults = {
            key: (group, label, index)
            for index, (key, _, group, label) in enumerate(DEFAULT_SITE_CONFIGS, start=1)
        }
        for key, value in configs.items():
            item = self.db.scalar(select(CmsSiteConfig).where(CmsSiteConfig.config_key == key))
            if item:
                item.config_value = value
                continue

            group, label, sort_order = known_defaults.get(key, ("custom", key, 999))
            self.db.add(
                CmsSiteConfig(
                    config_key=key,
                    config_value=value,
                    config_group=group,
                    label=label,
                    sort_order=sort_order,
                )
            )
        self.db.commit()
        return True
