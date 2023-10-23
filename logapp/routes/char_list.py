import asyncio
from datetime import datetime
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from litestar import MediaType, Request, get, post
from litestar.response import File

from logfetcher.cruds.characters import create_character
from logfetcher.cruds.logs import get_sorted_dungeon_ratings, get_sorted_raid_ratings
from logfetcher.cruds.rfuncs import get_character, get_rio_stream, get_all_characters_ids
from logfetcher.cruds.wlog_auth import get_token
from logfetcher.models.characters import Character, CharacterCreate
from logfetcher.models.zones import (
    DungCurrentSeason,
    RaidCurrent,
    RaidDiffuclty,
    Raids,
    RaidsDict,
    WLogsMapping,
)

from jinja2 import Environment, FileSystemLoader

@get("/list", media_type=MediaType.HTML)
async def list_all_trackable(request: Request) -> str:
    try:
        all_characters_ids: set[int] = get_all_characters_ids()
        char_list: list[Character] = []
        for id in all_characters_ids:
            char_list.append(get_character(id))
        env = Environment(
            loader=FileSystemLoader("logapp/web_templates/")
        )
        char_list.sort(key=lambda x: x.name)
        template = env.get_template("char_list.html")
        return template.render(characters = char_list)
    except Exception as e:
        request.logger.error(e)
        request.logger.error(e.with_traceback())

