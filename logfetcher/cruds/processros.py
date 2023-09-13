import re
from typing import Optional

from logfetcher.models.characters import Character


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def criteria(x):
    return int(x[2]) - int(x[1])


def find_character_id(page_text: str) -> int:
    pattern: list[str] = re.findall('"characterId":(\S+?)}', string=page_text)
    return int(pattern[0])


def get_timestamp_from_redis_stream(timer: str) -> int:
    return int(timer[: timer.find("-") - 3])


def create_daily_message(increases: list) -> str:
    res: str = ""
    for entity in increases[::-1]:
        res += f"{entity[0]}: {entity[1]} -> {entity[2]}\n"
    return res


def build_wlog_query(
    character: Character, zone_id: int, difficulty: Optional[int] = None
) -> str:
    query: str = (
        '''
    { 
        characterData
            {
			character (name: "'''
        + character.name
        + '''", serverSlug: "'''
        + character.wlog_server
        + '''", serverRegion: "'''
        + character.server_region
        + """")
                {
				encounterRankings (encounterID: """
        + str(zone_id)
    )

    if difficulty:
        query += ", difficulty: " + str(difficulty)

    query += """ ) 
				
			}
        }
    }
    """
    return query
