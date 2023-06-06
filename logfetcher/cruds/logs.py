import asyncio
from typing import Optional

import backoff
import httpx

from logfetcher.config import config
from logfetcher.cruds.processros import build_wlog_query
from logfetcher.cruds.wlog_auth import WOWLogsOAuth2Client
from logfetcher.models.characters import Character
from logfetcher.models.logs import WarcraftLogs
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
) -> list[float]:
    ex: WOWLogsOAuth2Client = WOWLogsOAuth2Client(
        config.wlog_id,
        config.wlog_secret,
    )
    ex.get_access_token()
    async with httpx.AsyncClient() as client:
        query: str = build_wlog_query(character, zone_id, difficulty)
        try:
            result: httpx.Response = fetch_logs(query, client, ex.access_token)
            logs: list[float] = process_character_ratings(result.json())
        except Exception as e:
            print(f"Error while log fetching: {e}")
    return logs


async def get_sorted_raid_ratings(
    character: Character, zone_id: dict, difficulty: Optional[int] = None
) -> list[float]:
    ex: WOWLogsOAuth2Client = WOWLogsOAuth2Client(
        config.wlog_id,
        config.wlog_secret,
    )
    ex.get_access_token()
    logs: dict[log_service.BossResponse] = {}
    task_group: asyncio.TaskGroup
    tasks: dict[asyncio.Task] = {}
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as task_group:
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


def process_character_ratings(character_data: str) -> list[float]:
    logs: WarcraftLogs = WarcraftLogs(data=character_data["data"])
    logs_percintile: list[float] = []
    for single_run in logs.data.characterData.character.encounterRankings.ranks:
        logs_percintile.append(int(single_run.historicalPercent))
    return sorted(logs_percintile)
