import discord
from loguru import logger

from dcbot.character_processors import process_dungeon, process_raid, add_character_to_watch
from dcbot.functions import check_message
from dcbot.guild_processors import add_guild_to_watch
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

    message_content: list[str] = message.content.split()

    if not len(message_content):
        logger.info(f"Recieved empty message from {message.author.name}. Skipping...")
        return
    
    if message_content[0] in ["!" + s.value for s in Dungeons]:
        await process_dungeon(message)
    elif message_content[0] in ["!" + s.value for s in Raids]:
        await process_raid(message)
    elif message_content[0] == "!ww" and message_content[1] == "add":
        if message_content[2] == "-g":
            await add_guild_to_watch(message)
        elif message_content[2] == "-c":
            await add_character_to_watch(message)        

    else:
        logger.info(
            f"Recieved message w/o WoW-bot request from {message.author.name}. Skipping..."
        )
