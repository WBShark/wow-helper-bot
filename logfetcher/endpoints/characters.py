from fastapi import APIRouter
from pydantic import HttpUrl

from logfetcher.cruds import characters, rfuncs
from logfetcher.cruds.rio_runs import fetch_all_runs_ids
from logfetcher.models.characters import Character, CharacterCreate
from logfetcher.models.zones import Dungeons, RioMapping, WLogsMapping

characters_router: APIRouter = APIRouter()


@characters_router.post("/", tags=["get_character_rating"])
async def get_character_ratings(char: CharacterCreate) -> dict:
    character = await characters.create_character(char)
    runs_ids: list[int] = await fetch_all_runs_ids(character)

    return {"runs": runs_ids}


@characters_router.post("/my-characters", tags=["my characters"])
async def add_my_character(char: CharacterCreate) -> dict:
    character = await characters.create_character(char)

    my_characters: list[int] = rfuncs.add_my_character(character)
    return {"characters": my_characters}


@characters_router.get("/my-characters", tags=["my characters"])
async def list_my_characters() -> dict:
    my_characters: list[int] = rfuncs.get_my_characters()
    return {"characters": my_characters}


@characters_router.delete("/my-characters", tags=["my characters"])
async def delete_all_my_characters() -> dict:
    return {"success": rfuncs.delete_all_my_characters()}
