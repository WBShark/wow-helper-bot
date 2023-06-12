from logfetcher.db_redis import db
from logfetcher.models.characters import Character
from typing import Set, Any

MYCHARS: str = "my_characters:rio:ids"


def add_my_character(character: Character) -> Set[Any]:
    db.sadd(MYCHARS, character.rio_id)
    return db.smembers(MYCHARS)


def delete_all_my_characters() -> int:
    return db.delete(MYCHARS)


def get_my_characters() -> Set[Any]:
    return db.smembers(MYCHARS)
