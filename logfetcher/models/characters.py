from typing import Optional

from pydantic import BaseModel, HttpUrl


class CharacterCreate(BaseModel):
    rio_url: HttpUrl


class Character(CharacterCreate):
    wlog_url: HttpUrl
    wid: Optional[int]
    rio_id: int
    name: str
    rio_server: str
    wlog_server: str
    server_region: str


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
