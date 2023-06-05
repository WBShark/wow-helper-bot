from logfetcher.db_redis import db
from logfetcher.models.characters import Character

MYCHARS: str = "my_characters:rio:ids"


def add_my_character(character: Character) -> list[int]:
    db.sadd(MYCHARS, character.rioid)
    return db.smembers(MYCHARS)


def delete_all_my_characters() -> bool:
    return db.delete(MYCHARS)


def get_my_characters() -> list[int]:
    return db.smembers(MYCHARS)
