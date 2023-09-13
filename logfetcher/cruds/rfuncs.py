import json
from typing import Any, Set

from logfetcher.config import ONE_HOUR
from logfetcher.cruds.processros import get_timestamp_from_redis_stream
from logfetcher.cruds.rio_fetcher import get_character_rio_score
from logfetcher.db_redis import db
from logfetcher.models.characters import Character
from logfetcher.models.guild import Guild

MYCHARS: str = "my_characters:rio:ids"
GUILDS_IDS_TO_WATCH: str = "guilds_ids_to_watch"
CHARACTER_IDS_TO_WATCH: str = "character_ids_to_watch"


def guild_key(id: int) -> str:
    return "guild:" + str(id)


def guild_channel_key(id: int) -> str:
    return "guild:CHANNEL:" + str(id)


def character_key(id: int) -> str:
    return "character:" + str(id)


def character_STREAM_key(id: int) -> str:
    return "character:STREAM:" + str(id)


def get_character(character_id: int) -> Character:
    return Character(**json.loads(db.get(character_key(character_id))))


def set_guild_discord_channel(guild_id: int, channel_id: int) -> None:
    db.set(guild_channel_key(guild_id), str(channel_id))


def get_guild_discord_channel(guild_id: int) -> int:
    return int(db.get(guild_channel_key(guild_id)))


def get_guild(guild_id: int) -> Guild:
    return Guild(**json.loads(db.get(guild_key(guild_id))))


def get_rio_stream(character_id: int, min: str = "-", max: str = "+") -> Any:
    return db.xrange(character_STREAM_key(character_id), min, max)


def add_guild(guild: Guild) -> Set[Any]:
    db.sadd(GUILDS_IDS_TO_WATCH, guild.id)
    db.set(guild_key(guild.id), json.dumps(guild.dict()))
    for character in guild.members:
        db.sadd(CHARACTER_IDS_TO_WATCH, character.rio_id)
        db.set(character_key(character.rio_id), json.dumps(character.dict()))
    return db.get(guild_key(guild.id))


def get_all_characters_ids() -> set[int]:
    return set(map(int, db.smembers(CHARACTER_IDS_TO_WATCH)))


def get_all_guilds_ids() -> set[int]:
    return db.smembers(GUILDS_IDS_TO_WATCH)


async def update_rio_stream(character_id: int) -> None:
    character: Character = get_character(character_id=character_id)
    db.xadd(
        character_STREAM_key(character_id),
        {"rio_score": await get_character_rio_score(character)},
    )
    return character_id


def get_daily_increase(character_id: int) -> (Any, Any, Any, Any):
    rio_scores: list[Any] = get_rio_stream(character_id)
    character: Character = get_character(character_id)
    last_rio: int = rio_scores[-1]
    for score in rio_scores:
        if (
            get_timestamp_from_redis_stream(last_rio[0])
            - get_timestamp_from_redis_stream(score[0])
            >= 24 * ONE_HOUR / 1000
        ):
            return (
                character.name,
                score[1]["rio_score"],
                last_rio[1]["rio_score"],
                character.rio_id,
            )

    return (
        character.name,
        last_rio[1]["rio_score"],
        last_rio[1]["rio_score"],
        character.rio_id,
    )
