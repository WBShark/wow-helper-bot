import asyncio
from logging import Logger
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
    character: Character, zone: int, difficulty: Optional[int] = None
) -> list[float]:
    ex: WOWLogsOAuth2Client = WOWLogsOAuth2Client(
        config.wlog_id,
        config.wlog_secret,
    )
    ex.get_access_token()
    async with httpx.AsyncClient() as client:
        query: str = build_wlog_query(character, zone, difficulty)
        try:
            result: httpx.Response = fetch_logs(query, client, ex.access_token)
            logs: list[float] = process_character_ratings(result.json())
        except Exception as e:
            print(f"Error while log fetching: {e}")
    return logs


async def get_sorted_raid_ratings(
    character: Character, zone: dict, difficulty: Optional[int] = None
) -> list[float]:
    ex: WOWLogsOAuth2Client = WOWLogsOAuth2Client(
        config.wlog_id,
        config.wlog_secret,
    )
    ex.get_access_token()
    logs: dict[log_service.BossResponse] = {}
    tg: asyncio.TaskGroup
    tasks: dict[asyncio.Task] = {}
    async with httpx.AsyncClient() as client:
        async with asyncio.TaskGroup() as tg:
            for boss in zone:
                query: str = build_wlog_query(character, zone[boss], difficulty)
                try:
                    tasks[boss] = tg.create_task(
                        fetch_logs(query, client, ex.access_token)
                    )

                except Exception as e:
                    print(f"Error while log fetching: {e}")
    for boss, results in tasks.items():
        logs[boss] = log_service.BossResponse(
            rankings=process_character_ratings((results.result()).json())
        )
    return logs


def process_character_ratings(data: str) -> list[float]:
    logs: WarcraftLogs = WarcraftLogs(data=data["data"])
    results: list[float] = []
    for single_run in logs.data.characterData.character.encounterRankings.ranks:
        results.append(int(single_run.historicalPercent))
    return sorted(results)
