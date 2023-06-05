import backoff
import discord
import grpc
from loguru import logger
from pydantic import HttpUrl

import logfetcher.proto.log_service_pb2_grpc as log_service
from dpschecker.logs import LogInfo, RaidLogInfo
from logfetcher.models.zones import Dungeons, RaidDiffuclty, Raids
from logfetcher.proto.log_service_pb2 import (
    DRRequest,
    DRResponse,
    RRRequest,
    RRResponse,
)


def check_message(message: discord.message.Message) -> bool:
    if message.author.bot:
        logger.info(f"Recieved message from bot: {message.author.name}. Skipping...")
        return False
    return True


@backoff.on_exception(backoff.expo, grpc.RpcError, max_time=10)
async def process_dungeon_request(rio_url: HttpUrl, dungeoun: Dungeons) -> LogInfo:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub: log_service.LogFetcherStub = log_service.LogFetcherStub(channel)
        try:
            logger.info(f"Processing dungeoun {dungeoun} and character {rio_url}.")
            response: DRResponse = await stub.GetDungeonRanks(
                DRRequest(dung=dungeoun.value, rio_link=rio_url)
            )
            return LogInfo(rankings=list(response.rankings), name=response.name)
        except Exception as e:
            print(e)
            logger.error(
                f"Failed to process character for dungeoun {dungeoun} and character {rio_url} with error {e}"
            )


@backoff.on_exception(backoff.expo, grpc.RpcError, max_time=10)
async def process_raid_request(
    rio_url: HttpUrl, raid: Raids, dffc: RaidDiffuclty
) -> LogInfo:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub: log_service.LogFetcherStub = log_service.LogFetcherStub(channel)
        try:
            logger.info(f"Processing dungeoun {raid} and character {rio_url}.")
            response: RRResponse = await stub.GetRaidRanks(
                RRRequest(raid=raid.value, rio_link=rio_url, dfffc=dffc)
            )
            return RaidLogInfo(rankings=response.rankings, name=response.name)
        except Exception as e:
            print(e)
            logger.error(
                f"Failed to process character for dungeoun {raid} and character {rio_url} with error {e}"
            )


def pretify_message(rankings: str):
    a = list(map(int, rankings.split()))
    a.sort(reverse=True)
    n = len(a)
    s = []
    for i in range(n):
        if i == 0:
            if a[i] < 30:
                s.append("__" + str(a[i]) + "__ ")
            elif a[i] > 80:
                s.append("**" + str(a[i]) + "** ")
            else:
                s.append(str(a[i]))
        elif len(s) % 9 == 8:
            if a[i] < 30:
                s.append("\n")
                s.append("__" + str(a[i]) + "__ ")
            elif a[i] > 80:
                s.append("\n")
                s.append("**" + str(a[i]) + "** ")
            else:
                s.append("\n")
                s.append(str(a[i]))
        else:
            if a[i] < 30:
                s.append("__" + str(a[i]) + "__ ")
            elif a[i] > 80:
                s.append("**" + str(a[i]) + "** ")
            elif s[-1][-1] not in "1234567890":
                s.append(str(a[i]))
            else:
                s.append(" " + str(a[i]) + " ")
    f = ""
    for i in s:
        f += i
    return f
