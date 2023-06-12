import re
from typing import Optional

from logfetcher.models.characters import Character


def find_character_id(page_text: str) -> int:
    pattern: list[str] = re.findall('"characterId":(\S+?)}', string=page_text)
    return int(pattern[0])


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
