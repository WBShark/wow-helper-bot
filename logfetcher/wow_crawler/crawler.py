import asyncio
import logging
import time
from typing import Any

import discord

from logfetcher.config import ONE_HOUR, config
from logfetcher.cruds import guilds, logs, processros, rfuncs
from logfetcher.cruds.processros import create_daily_message, criteria
from logfetcher.cruds.rio_fetcher import crawl_character, crawl_guild
from logfetcher.models.characters import Character
from logfetcher.models.guild import Guild
from logfetcher.models.zones import (
    DungCurrentSeason,
    RaidCurrent,
    RaidDiffuclty,
    RaidsDict,
    WLogsMapping,
)

# from dcbot.bot import client


class MyClient(discord.Client):
    message: str = None

    def __init__(self, message, intents):
        self.message = message
        super(MyClient, self).__init__(intents=intents)

    async def on_ready(self) -> None:
        try:
            logging.warning(f"We have logged in as {self.user}")
            for guild_id in self.message:
                for channel_id in rfuncs.get_guild_discord_channel(guild_id):
                    channel = await self.fetch_channel(channel_id)
                    await channel.send(self.message[guild_id])
        except Exception as e:
            logging.error(e)

        await self.close()


def create_client(all_messages: dict) -> MyClient:
    intents: discord.Intents = discord.Intents.default()
    intents.message_content = True
    return MyClient(message=all_messages, intents=intents)


class WoWCrawler:
    last_crawl: int
    last_rio_score: int
    last_guild: int
    last_shout: int
    last_logs: int

    def __init__(self, current_time: int) -> None:
        self.last_crawl = current_time
        self.last_rio_score = current_time
        self.last_logs = current_time
        self.last_guild = current_time
        self.last_shout = current_time

    async def initial_actions(self) -> None:
        await self.crawl()
        await self.update_guilds()
        await self.update_character_info()
        await self.shout()
        return

    def crawl_outdated(self) -> bool:
        return time.time() - self.last_crawl > 3 * ONE_HOUR

    def rio_scores_outdated(self) -> bool:
        return time.time() - self.last_rio_score > 4 * ONE_HOUR

    def logs_outdated(self) -> bool:
        return time.time() - self.last_logs > 10

    def guild_outdated(self) -> bool:
        return time.time() - self.last_guild > 4 * ONE_HOUR

    def shout_outdated(self) -> bool:
        return time.time() - self.last_shout > 24 * ONE_HOUR

    async def update_character_info(self) -> bool:
        all_characters_ids: set[int] = rfuncs.get_all_characters_ids()
        logging.warning(f"Characters to update info: {all_characters_ids}")
        for chunk in processros.chunks(list(all_characters_ids), 10):
            try:
                coros = [
                    asyncio.create_task(rfuncs.update_rio_stream(character_id=char_id))
                    for char_id in chunk
                ]
            except Exception as e:
                logging.warning(e)
            processed_characters, _undone = await asyncio.wait(coros)
            for character in processed_characters:
                try:
                    logging.warning(f"Updated character rio: {character.result()}")
                except Exception:
                    continue
        self.last_rio_score = time.time()
        return

    async def update_character_logs(self) -> bool:
        all_characters_ids: set[int] = rfuncs.get_all_characters_ids()
        logging.warning(f"Characters to update logs: {all_characters_ids}")
        for character_id in all_characters_ids:
            character: Character = rfuncs.get_character(character_id)
            logging.warning(f"Updating logs for {character.name}")
            tasks: dict = {}
            async with asyncio.TaskGroup() as tg:
                for dffclt in RaidDiffuclty:
                    if dffclt == 0:
                        continue
                    tasks[RaidCurrent.value + str(dffclt.value)] = tg.create_task(
                        logs.get_sorted_raid_ratings(
                            character, RaidsDict[RaidCurrent.value], dffclt.value
                        )
                    )
                for dung in DungCurrentSeason:
                    tasks[dung.value] = tg.create_task(
                        logs.get_sorted_dungeon_ratings(
                            character, WLogsMapping[dung.value]
                        )
                    )
            for key in tasks:
                rfuncs.set_character_zone_logs(character_id, key, tasks[key].result())
        self.last_logs = time.time()
        return

    async def update_guilds(self) -> True:
        all_guilds_ids: set[int] = rfuncs.get_all_guilds_ids()
        for guild_id in all_guilds_ids:
            guild: Guild = rfuncs.get_guild(guild_id)
            logging.warning(f"Updating guild: {guild.name}")
            await guilds.add_guild_to_watcher(guild.rio_url, None)
        self.last_guild = time.time()
        return bool

    async def crawl(self) -> bool:
        all_characters_ids: set[int] = rfuncs.get_all_characters_ids()
        all_guilds_ids: set[int] = rfuncs.get_all_guilds_ids()
        logging.warning(f"Guilds to crawl: {all_guilds_ids}")
        for chunk in processros.chunks(list(all_guilds_ids), 10):
            try:
                coros = [
                    asyncio.create_task(crawl_guild(rfuncs.get_guild(guild_id)))
                    for guild_id in chunk
                ]
            except Exception as e:
                logging.warning(e)
            processed_guilds, _undone = await asyncio.wait(coros)
            for guild_list in processed_guilds:
                try:
                    for id in guild_list.result():
                        if id in all_characters_ids:
                            all_characters_ids.remove(id)
                    logging.warning(f"Crawled characters: {guild_list.result()}")
                except Exception as e:
                    logging.warning(e)

        logging.warning(f"Characters to crawl: {all_characters_ids}")
        for chunk in processros.chunks(list(all_characters_ids), 10):
            try:
                coros = [
                    asyncio.create_task(crawl_character(rfuncs.get_character(char_id)))
                    for char_id in chunk
                ]
            except Exception as e:
                logging.warning(e)
            processed_characters, _undone = await asyncio.wait(coros)
            for character_id in processed_characters:
                try:
                    logging.warning(f"Crawled character: {character_id.result()}")
                    all_characters_ids.remove(id)
                except Exception:
                    continue
        self.last_crawl = time.time()
        return True

    async def shout(self) -> bool:
        all_guilds_ids: set[int] = rfuncs.get_all_guilds_ids()
        all_messages: dict = {}
        for guild_id in all_guilds_ids:
            all_increases: list[Any] = []
            guild: Guild = rfuncs.get_guild(guild_id)
            for member in guild.members:
                all_increases.append(rfuncs.get_daily_increase(member.rio_id))
            all_increases = sorted(all_increases, key=lambda x: criteria(x))[-5:]
            msg: str = (
                "Top 5 M+ score increases for nearly last 24 hours:\n"
                + create_daily_message(all_increases)
            )
            all_messages[guild_id] = msg
        client: MyClient = create_client(all_messages)
        await client.start(config.dc_bot_token)
        client.clear()
        self.last_shout = time.time()
        return 1
