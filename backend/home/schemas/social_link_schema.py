from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SocialLinkInput(BaseModel):
    id: int | None = None
    name: str = Field(min_length=1, max_length=64)
    icon: str = Field(min_length=1, max_length=500)
    tip: str = Field(min_length=1, max_length=255)
    url: str = Field(min_length=1, max_length=500)
    sort_order: int | None = Field(default=None, alias="sortOrder")
    enabled_flag: int | None = Field(default=None, alias="enabledFlag")

    model_config = ConfigDict(populate_by_name=True)


class SocialLinkResponse(BaseModel):
    id: int
    name: str | None
    icon: str | None
    tip: str | None
    url: str | None
    sort_order: int = Field(alias="sortOrder")
    enabled_flag: int = Field(alias="enabledFlag")
    create_time: datetime | None = Field(alias="createTime")
    update_time: datetime | None = Field(alias="updateTime")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
