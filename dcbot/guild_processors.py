import signal

import discord
import grpc  # type: ignore
from loguru import logger

import logfetcher.proto.log_service_pb2_grpc as log_service
from dcbot.config import config
from logfetcher.proto.log_service_pb2 import GuildAddRequest, GuildAddResponse


def handler(signum, frame) -> None:
    logger.error("Timeout hits for requst processing!")
    raise Exception("Timeout")


signal.signal(signal.SIGALRM, handler)


async def add_guild_to_watch(message: discord.message.Message) -> None:
    async with grpc.aio.insecure_channel(
        ":".join(["localhost", config.grpc_port])
    ) as channel:
        try:
            grpc_stub: log_service.LogFetcherStub = log_service.LogFetcherStub(channel)
            logger.error(message.channel.id)
            response: GuildAddResponse = await grpc_stub.AddGuildToWathcer(
                GuildAddRequest(
                    rio_guild_link=message.content.split()[-1],
                    channel_id=str(message.channel.id),
                )
            )
            await message.reply(
                f"Guild added to watcher successfully with id: {response.rd_guild_id}"
            )
        except Exception as e:
            logger.error(e)
            await message.reply("Cant now, error")
