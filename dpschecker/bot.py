import discord
from loguru import logger

from dpschecker.functions import check_message
from dpschecker.logs import LogInfo
from dpschecker.processors import process_dungeon, process_raid
from logfetcher.models.zones import Dungeons, Raids

intents: discord.Intents = discord.Intents.default()
intents.message_content = True

client: discord.Client = discord.Client(intents=intents)


@client.event
async def on_ready() -> None:
    logger.info(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.message.Message) -> None:
    if not check_message(message):
        logger.info(f"Skipping message {message.id} from {message.author.name}.")
        return

    content = message.content.split()

    if content[0] in ["!" + s.value for s in Dungeons]:
        await process_dungeon(message)
    elif content[0] in ["!" + s.value for s in Raids]:
        await process_raid(message)
    else:
        logger.info(
            f"Recieved message w/o WoW-bot request from {message.author.name}. Skipping..."
        )

    return
