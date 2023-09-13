from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class CharacterCreate(BaseModel):
    rio_url: HttpUrl = Field(alias="profile_url")

    class Config:
        allow_population_by_field_name = True


class Character(CharacterCreate):
    wlog_url: HttpUrl
    wid: Optional[int]
    rio_id: int
    name: str
    rio_server: str
    wlog_server: str
    server_region: str
    realm_id: Optional[int]
    realm_name: Optional[str]


class Realm(BaseModel):
    id: int
    connectedRealmId: int
    name: str
    altName: str
    slug: str
    altSlug: str
    locale: str
    isConnected: str


class CharacterInfo(BaseModel):
    id: int
    name: str
    realm: Realm
    region: dict


class CharacterDetails(BaseModel):
    character: CharacterInfo


class CharacterRioData(BaseModel):
    characterDetails: CharacterDetails
