import json

import httpx

from logfetcher.models.characters import Character
from logfetcher.models.zones import Dungeons, RioMapping


def request_url(character_id: int, dungeon_id: int) -> str:
    return (
        "https://raider.io/api/characters/mythic-plus-runs?season=season-df-1&characterId="
        + str(character_id)
        + "&dungeonId="
        + str(dungeon_id)
        + "&role=all&specId=0&mode=scored&affixes=all&date=all"
    )


async def fetch_runs_ids_for_dungeon(character: Character, dungeon_id: int) -> list[int]:
    async with httpx.AsyncClient() as client:
        character_all_runs_data: dict = json.loads((await client.get(request_url(character.rio_id, dungeon_id))).text)
        all_single_dungeon_runs: list[int] = []
        for single_run in character_all_runs_data["runs"]:
            all_single_dungeon_runs.append(int(single_run["summary"]["keystone_run_id"]))
        return all_single_dungeon_runs


async def fetch_all_runs_ids(character: Character) -> list[int]:
    all_runs: list[int] = []
    for dungeon in Dungeons:
        all_runs.append(
            await fetch_runs_ids_for_dungeon(character, RioMapping[dungeon.value])
        )
    
    return [run for dungeon in all_runs for run in dungeon]
