from typing import Optional

from pydantic import BaseModel, HttpUrl


class CharacterCreate(BaseModel):
    rio_url: HttpUrl


class Character(CharacterCreate):
    wlog_url: HttpUrl
    wid: Optional[int]
    rioid: int
    name: str
    rio_server: str
    wlog_server: str
    server_region: str
