from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SiteConfigItem(BaseModel):
    config_key: str = Field(alias="configKey")
    config_value: str | None = Field(default=None, alias="configValue")
    config_group: str = Field(alias="configGroup")
    label: str | None = None
    sort_order: int = Field(alias="sortOrder")
    create_time: datetime | None = Field(default=None, alias="createTime")
    update_time: datetime | None = Field(default=None, alias="updateTime")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SiteConfigSaveInput(BaseModel):
    configs: dict[str, str | None] = Field(default_factory=dict)
