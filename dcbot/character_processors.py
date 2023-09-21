import signal

import discord
from loguru import logger
from pydantic import HttpUrl

import grpc  # type: ignore

import logfetcher.proto.log_service_pb2_grpc as log_service
from dcbot.config import config
from logfetcher.proto.log_service_pb2 import CharacterAddRequest, CharacterAddResponse

from dcbot.functions import (
    pretify_message,
    process_dungeon_request,
    process_raid_request,
)
from dcbot.logs import LogInfo, RaidLogInfo
from logfetcher.models.zones import Dungeons, RaidDiffuclty, Raids
from logfetcher.proto.log_service_pb2 import BossResponse


def handler(signum, frame) -> None:
    logger.error("Timeout hits for requst processing!")
    raise Exception("Timeout")


signal.signal(signal.SIGALRM, handler)


async def process_raid(message: discord.message.Message) -> None:
    try:
        rio_url: HttpUrl = HttpUrl(url=message.content.split()[-1], scheme="https")
        difficulty: RaidDiffuclty = RaidDiffuclty.All
        raid: Raids = Raids(message.content.split()[0][1:])
    except Exception as e:
        logger.error(
            f"Failed to parse raid and character in message from {message.author.name} due to {e}"
        )
        return
    signal.alarm(1000)
    try:
        loginfo: RaidLogInfo = await process_raid_request(rio_url, raid, difficulty)
    except Exception as e:
        logger.error(
            f"Failed to process raid request from {message.author.name} with error {e}"
        )
    signal.alarm(0)
    try:
        logs_summary: str = (
            f"Logs' percentile for raid {raid.value}:{difficulty.name if difficulty else 'Normal'}"
            + f"and character {loginfo.name}\n"
        )

        if len(loginfo.rankings):
            rankings: str = ""
            boss: str
            reports: BossResponse
            for boss, reports in loginfo.rankings.items():
                rankings = rankings + boss.upper() + ": "
                for single_kill in reports.rankings:
                    rankings = rankings + str(single_kill) + " "
                rankings += "\n"
            logs_summary += rankings
        else:
            logs_summary += f"```There is no ranked runs for {raid.value}```"
        await message.reply(logs_summary)
    except Exception as e:
        logger.error(
            f"Failed to send report message for raid {raid.value} and character {loginfo.name} with {e}"
        )


async def process_dungeon(message: discord.message.Message) -> None:
    try:
        rio_url: HttpUrl = HttpUrl(url=message.content.split()[-1], scheme="https")
        dungeoun: Dungeons = Dungeons(message.content.split()[0][1:])
    except Exception as e:
        logger.error(
            f"Failed to parse dungeoun and character in message from {message.author.name} due to {e}"
        )
        return
    signal.alarm(1000)
    try:
        loginfo: LogInfo = await process_dungeon_request(rio_url, dungeoun)
    except Exception as e:
        logger.error(
            f"Failed to process rd request from {message.author.name} with error {e}"
        )
    signal.alarm(0)
    try:
        logs_summary: str = f"Logs' percentile for dungeoun {dungeoun.value} and character {loginfo.name}\n"
        if len(loginfo.rankings):
            rankings = ""
            for single_run in loginfo.rankings:
                rankings += str(round(float(single_run))) + " "

            # await message.channel.send(logs_summary)
            logs_summary = logs_summary + "```" + pretify_message(rankings) + "```"
        else:
            logs_summary += f"```There is no ranked runs for {dungeoun.value}```"
        await message.reply(logs_summary)
    except Exception as e:
        logger.error(
            (
                f"Failed to send report message for dungeoun {dungeoun.value}",
                f"and character {loginfo.name} with {e}",
            )
        )

async def add_character_to_watch(message: discord.message.Message) -> None:
    async with grpc.aio.insecure_channel(
        ":".join(["localhost", config.grpc_port])
    ) as channel:
        try:
            grpc_stub: log_service.LogFetcherStub = log_service.LogFetcherStub(channel)
            logger.error(message.channel.id)
            response: CharacterAddResponse = await grpc_stub.AddCharacterToWathcer(
                CharacterAddRequest(
                    rio_character_link=message.content.split()[-1],
                    channel_id=str(message.channel.id),
                )
            )
            await message.reply(
                f"Character added to watcher successfully with id: {response.rd_char_id}"
            )
        except Exception as e:
            logger.error(e)
            await message.reply("Cant now, error")