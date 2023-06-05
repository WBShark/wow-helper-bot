from fastapi import APIRouter
from pydantic import HttpUrl

import logfetcher.models.characters as chars
from logfetcher.cruds import characters, logs
from logfetcher.models.logs import LogInfo
from logfetcher.models.zones import Dungeons, WLogsMapping, Zone

ranks_router: APIRouter = APIRouter()


@ranks_router.post("/dungeon/", tags=["rank_for_dungeon"])
async def rank_for_dungeon(
    rio_url: chars.CharacterCreate, dungeon: Dungeons
) -> LogInfo:
    print(WLogsMapping[dungeon.value])
    character: chars.Character = await characters.create_character(rio_url)
    rankings = await logs.get_sorted_raw_ratings(character, WLogsMapping[dungeon.value])
    return {"rankings": rankings, "name": character.name}
