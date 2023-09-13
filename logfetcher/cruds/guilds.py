import asyncio
import json
import logging

import httpx
from pydantic import HttpUrl

from logfetcher.cruds.characters import create_character, get_rio_initial_data
from logfetcher.cruds.processros import chunks
from logfetcher.cruds.rfuncs import add_guild, set_guild_discord_channel
from logfetcher.models.characters import Character, CharacterCreate
from logfetcher.models.guild import Guild, GuildCreate


async def add_guild_to_watcher(rio_link: HttpUrl, channel_id: int) -> str:
    rio_initial_data: dict = await get_rio_initial_data(rio_link)
    guild_create: GuildCreate = GuildCreate(
        id=rio_initial_data["guildDetails"]["guild"]["id"],
        name=rio_initial_data["guildDetails"]["guild"]["name"],
        region=rio_initial_data["guildDetails"]["guild"]["region"]["slug"],
        realm=rio_initial_data["guildDetails"]["guild"]["realm"]["slug"],
        realm_id=rio_initial_data["guildDetails"]["guild"]["realm"]["id"],
        realm_name=rio_initial_data["guildDetails"]["guild"]["realm"]["name"],
    )

    async with httpx.AsyncClient() as client:
        params: dict = {
            "region": guild_create.region,
            "realm": guild_create.realm,
            "name": guild_create.name,
            "fields": "members",
        }
        guild_info: httpx.Response = await client.get(
            "https://raider.io/api/v1/guilds/profile", params=params
        )
    guild_members: list[Character] = []
    guild_dict: dict = json.loads(guild_info.text)

    for chunk in chunks(guild_dict["members"], 10):
        try:
            coros = [
                asyncio.create_task(
                    create_character(
                        CharacterCreate(profile_url=char["character"]["profile_url"])
                    )
                )
                for char in chunk
            ]
        except Exception:
            logging.warning("error")
        processed_characters, _undone = await asyncio.wait(coros)
        for character in processed_characters:
            try:
                guild_members.append(character.result())
            except Exception:
                continue
    guild_to_add: Guild = Guild(
        **guild_create.dict(), members=guild_members, profile_url=rio_link
    )
    add_guild(guild_to_add)
    logging.warning(f"Guild {guild_to_add.name}channel: {channel_id}")
    set_guild_discord_channel(guild_to_add.id, channel_id)
    return guild_create.id
