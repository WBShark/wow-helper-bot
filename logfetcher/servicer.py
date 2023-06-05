import asyncio
import logging

import logfetcher.models.characters as chars
import logfetcher.proto.log_service_pb2 as log_service
import logfetcher.proto.log_service_pb2_grpc as log_service_grpc
from logfetcher.cruds import characters, logs
from logfetcher.models.zones import RaidsDict, WLogsMapping

### create task try


class LogFetcherServicer(log_service_grpc.LogFetcherServicer):
    def __init__(self):
        pass

    async def GetDungeonRanks(
        self, request: log_service.DRRequest, context
    ) -> log_service.DRResponse:
        logging.info(f"Get request for {request.dung} and character {request.rio_link}")
        char: chars.CharacterCreate = chars.CharacterCreate(rio_url=request.rio_link)
        character: chars.Character = await characters.create_character(char)
        dung_task: asyncio.Task = asyncio.create_task(
            logs.get_sorted_dungeon_ratings(character, WLogsMapping[request.dung])
        )
        await dung_task
        rankings = dung_task.result()
        return log_service.DRResponse(name=character.name, rankings=rankings)

    async def GetRaidRanks(
        self, request: log_service.RRRequest, context
    ) -> log_service.RRResponse:
        logging.info(f"Get request for {request.raid} and character {request.rio_link}")
        char: chars.CharacterCreate = chars.CharacterCreate(rio_url=request.rio_link)
        character: chars.Character = await characters.create_character(char)
        raid_task: asyncio.Task = asyncio.create_task(
            logs.get_sorted_raid_ratings(
                character, RaidsDict[request.raid], request.dfffc
            )
        )
        await raid_task
        rankings = raid_task.result()
        response = log_service.RRResponse(name=character.name, rankings=rankings)
        return response
