from pydantic import BaseModel


class AdminInfo(BaseModel):
    username: str
    nickname: str
