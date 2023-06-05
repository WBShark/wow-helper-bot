import json

import httpx

from logfetcher.cruds.wlog_auth import WOWLogsOAuth2Client
from logfetcher.models.characters import Character
from logfetcher.models.logs import WarcraftLogs
from logfetcher.models.zones import Dungeons, RioMapping


def request_url(id: int, dungeon: int) -> str:
    return (
        "https://raider.io/api/characters/mythic-plus-runs?season=season-df-1&characterId="
        + str(id)
        + "&dungeonId="
        + str(dungeon)
        + "&role=all&specId=0&mode=scored&affixes=all&date=all"
    )


async def fetch_runs_ids_for_dungeon(character: Character, dungeon: int) -> list[int]:
    client: httpx.AsyncClient = httpx.AsyncClient()
    response: httpx.Response = await client.get(request_url(character.rioid, dungeon))
    data: dict = json.loads(response.text)
    runs: list[int] = []
    for single_run in data["runs"]:
        runs.append(int(single_run["summary"]["keystone_run_id"]))
    return runs


async def fetch_all_runs_ids(character: Character) -> list[int]:
    all_runs: list[int] = []
    for dungeon in Dungeons:
        all_runs.append(
            await fetch_runs_ids_for_dungeon(character, RioMapping[dungeon.value])
        )

    return [run for dungeon in all_runs for run in dungeon]
