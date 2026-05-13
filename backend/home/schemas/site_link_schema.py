from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SiteLinkInput(BaseModel):
    id: int | None = None
    icon: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=64)
    link: str = Field(min_length=1, max_length=500)
    sort_order: int | None = Field(default=None, alias="sortOrder")
    enabled_flag: int | None = Field(default=None, alias="enabledFlag")

    model_config = ConfigDict(populate_by_name=True)


class SiteLinkResponse(BaseModel):
    id: int
    icon: str | None
    name: str | None
    link: str | None
    sort_order: int = Field(alias="sortOrder")
    enabled_flag: int = Field(alias="enabledFlag")
    create_time: datetime | None = Field(alias="createTime")
    update_time: datetime | None = Field(alias="updateTime")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
