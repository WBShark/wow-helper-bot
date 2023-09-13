import logging
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
from litestar import MediaType, get, post
from litestar.response import File

from logfetcher.cruds.characters import create_character
from logfetcher.cruds.logs import get_sorted_raid_ratings
from logfetcher.cruds.rfuncs import get_rio_stream
from logfetcher.models.characters import Character, CharacterCreate
from logfetcher.models.zones import Raids, RaidsDict

FOLDER_SUFFIX: str = "logapp/routes/"


@post("/")
async def pull_raid_hist_stats(char_url: str, raid: Raids) -> dict[str, list[str]]:
    char: Character = await create_character(CharacterCreate(rio_url=char_url))
    logs: dict[str, list[str]] = await get_sorted_raid_ratings(char, RaidsDict["atsc"])
    return logs


@get("/image/{character_id:int}")
async def get_image(character_id: int) -> File:
    stream = await get_rio_stream(character_id)
    x_axis: list[str] = []
    y_axis: list[float] = []
    try:
        for entry in stream:
            x_axis.append(
                datetime.fromtimestamp(int(entry[0][0 : entry[0].find("-") - 3]))
            )
            y_axis.append(entry[1]["rio_score"])
        plt.plot(x_axis, y_axis)
    except Exception as e:
        logging.error(e)
        print(e)
    image_name: str = "-".join(["rio", str(character_id)]) + ".png"
    plt.savefig("".join([FOLDER_SUFFIX, image_name]))
    return File(
        path=Path(Path(__file__).resolve().parent, image_name).with_suffix(".png"),
        filename=image_name,
    )


@get("/{character_id:int}", media_type=MediaType.HTML)
async def get_char_graph(character_id: int) -> str:
    return f"""
            <html>
                <body>
                    <div>
                        <img src="image/{character_id}" alt="Italian Trulli" />
                    </div>
                </body>
            </html>
        """
