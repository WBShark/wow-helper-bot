import asyncio
from typing import Iterable, Optional

import backoff
import httpx

from logfetcher.config import config
from logfetcher.cruds.processros import build_wlog_query
from logfetcher.cruds.wlog_auth import WOWLogsOAuth2Client
from logfetcher.models.characters import Character
from logfetcher.models.logs import Data, WarcraftLogs
from logfetcher.proto import log_service_pb2 as log_service


@backoff.on_exception(backoff.expo, httpx.HTTPError, max_time=10)
async def fetch_logs(
    query: str, client: httpx.AsyncClient, access_token: str
) -> httpx.Response:
    return await client.post(
        "https://www.warcraftlogs.com/api/v2/client",
        headers={
            "Content-Type": "application/json",
            "authorization": "Bearer " + access_token,
        },
        json={"query": query},
        timeout=1,
    )


async def get_sorted_dungeon_ratings(
    character: Character, zone_id: int, difficulty: Optional[int] = None
) -> Optional[Iterable[int]]:
    ex: WOWLogsOAuth2Client = WOWLogsOAuth2Client(
        config.wlog_id,
        config.wlog_secret,
    )
    ex.get_access_token()
    async with httpx.AsyncClient() as client:
        query: str = build_wlog_query(character, zone_id, difficulty)
        try:
            result: httpx.Response = await fetch_logs(query, client, ex.access_token)
            logs: Optional[Iterable[int]] = process_character_ratings(result.json())
        except Exception as e:
            print(f"Error while log fetching: {e}")
    return logs


async def get_sorted_raid_ratings(
    character: Character, zone_id: dict, difficulty: Optional[int] = None
) -> dict[str, log_service.BossResponse]:
    ex: WOWLogsOAuth2Client = WOWLogsOAuth2Client(
        config.wlog_id,
        config.wlog_secret,
    )
    ex.get_access_token()
    logs: dict[str, log_service.BossResponse] = {}
    task_group: asyncio.taskgroups.TaskGroup
    tasks: dict[str, asyncio.Task] = {}
    async with httpx.AsyncClient() as client:
        async with asyncio.taskgroups.TaskGroup() as task_group:
            for boss in zone_id:
                query: str = build_wlog_query(character, zone_id[boss], difficulty)
                try:
                    tasks[boss] = task_group.create_task(
                        fetch_logs(query, client, ex.access_token)
                    )

                except Exception as e:
                    print(f"Error while log fetching: {e}")
    for boss, results in tasks.items():
        logs[boss] = log_service.BossResponse(
            rankings=process_character_ratings((results.result()).json())
        )
    return logs


def process_character_ratings(character_data: dict) -> Optional[Iterable[int]]:
    logs: WarcraftLogs = WarcraftLogs(data=Data.parse_obj(character_data["data"]))
    logs_percintile: list[int] = []
    if logs.data.characterData.character.encounterRankings.ranks:
        for single_run in logs.data.characterData.character.encounterRankings.ranks:
            logs_percintile.append(int(single_run.historicalPercent))
        return logs_percintile.sort()
    else:
        return []
