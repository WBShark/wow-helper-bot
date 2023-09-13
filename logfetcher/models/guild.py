from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from logfetcher.models.characters import Character


class GuildCreate(BaseModel):
    id: int
    region: str
    realm: str
    name: str
    realm_id: Optional[int]
    realm_name: Optional[str]


class Guild(GuildCreate):
    members: list[Character]
    rio_url: HttpUrl = Field(alias="profile_url")

    class Config:
        allow_population_by_field_name = True
