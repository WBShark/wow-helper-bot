import json

import httpx

from logfetcher.models.characters import Character
from logfetcher.models.guild import Guild
from logfetcher.models.zones import Dungeons, RioMapping


async def crawl_character(character: Character) -> bool:
    async with httpx.AsyncClient() as client:
        params: dict = {
            "realmId": character.realm_id,
            "realm": character.realm_name,
            "region": character.rio_server,
            "character": character.name,
        }
        _crawl_result: httpx.Response = await client.post(
            "https://raider.io/api/crawler/characters", params=params
        )
    return character.rio_id


async def crawl_guild(guild: Guild) -> list[int]:
    async with httpx.AsyncClient() as client:
        params: dict = {
            "realmId": guild.realm_id,
            "realm": guild.realm_name,
            "region": guild.region,
            "guild": guild.name,
            "numMembers": 0,
        }
        _crawl_result: httpx.Response = await client.post(
            "https://raider.io/api/crawler/guilds", params=params
        )
    return [member.rio_id for member in guild.members]


async def get_character_rio_score(character: Character) -> int:
    async with httpx.AsyncClient() as client:
        params: dict = {
            "region": character.server_region,
            "realm": character.rio_server,
            "name": character.name,
            "fields": "mythic_plus_scores_by_season:current",
        }
        mplus_run_info: httpx.Response = await client.get(
            "https://raider.io/api/v1/characters/profile", params=params
        )
    mplus_json: dict = json.loads(mplus_run_info.text)
    return int(mplus_json["mythic_plus_scores_by_season"][0]["scores"]["all"])


def request_url(character_id: int, dungeon_id: int) -> str:
    return (
        "https://raider.io/api/characters/mythic-plus-runs?season=season-df-1&characterId="
        + str(character_id)
        + "&dungeonId="
        + str(dungeon_id)
        + "&role=all&specId=0&mode=scored&affixes=all&date=all"
    )


async def fetch_runs_ids_for_dungeon(
    character: Character, dungeon_id: int
) -> list[int]:
    async with httpx.AsyncClient() as client:
        character_all_runs_data: dict = json.loads(
            (await client.get(request_url(character.rio_id, dungeon_id))).text
        )
        all_single_dungeon_runs: list[int] = []
        for single_run in character_all_runs_data["runs"]:
            all_single_dungeon_runs.append(
                int(single_run["summary"]["keystone_run_id"])
            )
        return all_single_dungeon_runs


async def fetch_all_runs_ids(character: Character) -> list[int]:
    all_runs: list[list[int]] = []
    for dungeon in Dungeons:
        all_runs.append(
            await fetch_runs_ids_for_dungeon(character, RioMapping[dungeon.value])
        )

    return [run for dungeon in all_runs for run in dungeon]
