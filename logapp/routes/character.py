from litestar import post
from pydantic import HttpUrl

from logfetcher.cruds.characters import create_character
from logfetcher.cruds.logs import get_sorted_raid_ratings
from logfetcher.models.characters import Character, CharacterCreate
from logfetcher.models.zones import Raids, RaidsDict


@post("/")
async def pull_raid_hist_stats(char_url: str, raid: Raids) -> dict[str, list[str]]:
    char: Character = await create_character(CharacterCreate(rio_url=char_url))
    logs: dict[str, list[str]] = await get_sorted_raid_ratings(char, RaidsDict["atsc"])
    return logs
