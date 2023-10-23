import asyncio
from datetime import datetime
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from litestar import MediaType, Request, get, post
from litestar.response import File

from logfetcher.cruds.characters import create_character
from logfetcher.cruds.logs import get_sorted_dungeon_ratings, get_sorted_raid_ratings
from logfetcher.cruds.rfuncs import get_character, get_rio_stream
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

FOLDER_SUFFIX: str = "logapp/routes/"
PLOT_WIDTH: int = 4
PLOT_HEIGHT: int = 3


@post("/")
async def pull_raid_hist_stats(char_url: str, raid: Raids) -> dict[str, list[str]]:
    char: Character = await create_character(CharacterCreate(rio_url=char_url))
    logs: dict[str, list[str]] = await get_sorted_raid_ratings(char, RaidsDict["atsc"])
    return logs


@get("/image/info/{character_id:int}")
async def get_info_image(request: Request, character_id: int) -> File:
    try:
        stream = get_rio_stream(character_id)
        x_rio_axis: list[str] = []
        y_rio_axis: list[float] = []
        x_gear_axis: list[str] = []
        y_gear_axis: list[float] = []
        figure, axis = plt.subplots(1, 2, figsize=(PLOT_WIDTH * 3, PLOT_HEIGHT))
        for entry in stream:
            x_rio_axis.append(
                datetime.fromtimestamp(int(entry[0][0 : entry[0].find("-") - 3]))
            )
            y_rio_axis.append(entry[1]["rio_score"])
            if "ilvl" in entry[1].keys():
                x_gear_axis.append(
                    datetime.fromtimestamp(int(entry[0][0 : entry[0].find("-") - 3]))
                )
                y_gear_axis.append(entry[1]["ilvl"])
        axis[0].plot(x_rio_axis, y_rio_axis)
        axis[1].plot(x_gear_axis, y_gear_axis)
        figure.autofmt_xdate()
        image_name: str = "-".join(["info", str(character_id)]) + ".png"
        plt.savefig(
            "".join([FOLDER_SUFFIX, image_name]),
        )
        plt.cla()
        return File(
            path=Path(Path(__file__).resolve().parent, image_name).with_suffix(".png"),
            filename=image_name,
        )
    except Exception as e:
        request.logger.error(e)


@get("/image/logs/raids/{character_id:int}")
async def get_logs_raid_image(request: Request, character_id: int) -> File:
    try:
        character: Character = get_character(character_id)
        axis: list[plt.Axes]
        tasks = []
        token = get_token()
        async with asyncio.TaskGroup() as tg:
            tasks.append(
                tg.create_task(
                    get_sorted_raid_ratings(
                        character,
                        RaidsDict[RaidCurrent.value],
                        RaidDiffuclty.Normal.value,
                        token,
                    )
                )
            )
            tasks.append(
                tg.create_task(
                    get_sorted_raid_ratings(
                        character,
                        RaidsDict[RaidCurrent.value],
                        RaidDiffuclty.Heroic.value,
                        token,
                    )
                )
            )
            tasks.append(
                tg.create_task(
                    get_sorted_raid_ratings(
                        character,
                        RaidsDict[RaidCurrent.value],
                        RaidDiffuclty.Mythic.value,
                        token,
                    )
                )
            )

        num_plots: int = 0
        for i in range(len(tasks)):
            if any(list(tasks[i].result().values())):
                num_plots += 1

        if num_plots == 0:
            return None
        figure, axis = plt.subplots(
            1,
            num_plots,
            figsize=(PLOT_WIDTH * 3, PLOT_HEIGHT),
            sharex=False,
            sharey=False,
        )

        for i in range(num_plots):
            bosses = list(tasks[i].result().keys())
            kill_logs = list(tasks[i].result().values())
            y_logs = [val for data in kill_logs for val in data]
            x_logs = [
                bosses[i] for i, data in enumerate(kill_logs) for j in range(len(data))
            ]
            axis[i].scatter(x_logs, y_logs)
            axis[i].tick_params(axis="x", labelrotation=30)
            axis[i].set_ylim([0, 100])
        image_name: str = "-".join(["logs_raid", str(character_id)]) + ".png"
        figure.savefig(
            "".join([FOLDER_SUFFIX, image_name]),
        )
        return File(
            path=Path(Path(__file__).resolve().parent, image_name).with_suffix(".png"),
            filename=image_name,
        )
    except Exception as e:
        request.logger.error(e)
        request.logger.error(e.with_traceback())


@get("/image/logs/dungs/{character_id:int}")
async def get_logs_dungs_image(request: Request, character_id: int) -> File:
    try:
        character: Character = get_character(character_id)
        figure, axis = plt.subplots(
            1, 1, figsize=(PLOT_WIDTH * 3, PLOT_HEIGHT), sharex=False, sharey=False
        )
        tasks = {}
        token = get_token()
        async with asyncio.TaskGroup() as tg:
            for dung in DungCurrentSeason:
                tasks[dung.value] = tg.create_task(
                    get_sorted_dungeon_ratings(
                        character, WLogsMapping[dung.value], token=token
                    )
                )
        ll = {}
        for dung in tasks:
            ll[dung] = tasks[dung].result()
        bosses = list(ll.keys())
        kill_logs = list(ll.values())
        y_logs = [val for data in kill_logs for val in data]
        x_logs = [
            bosses[i] for i, data in enumerate(kill_logs) for j in range(len(data))
        ]
        axis.scatter(x_logs, y_logs)
        axis.set_ylim([0, 100])
        image_name: str = "-".join(["logs_dungs", str(character_id)]) + ".png"
        figure.savefig(
            "".join([FOLDER_SUFFIX, image_name]),
        )
        return File(
            path=Path(Path(__file__).resolve().parent, image_name).with_suffix(".png"),
            filename=image_name,
        )
    except Exception as e:
        request.logger.error(e)
        request.logger.error(e.with_traceback())


@get("/{character_id:int}", media_type=MediaType.HTML)
async def get_char_graph(character_id: int) -> str:
    return f"""
            <html>
                <body>
                    <div>
                        <img src="image/info/{character_id}" alt="Italian Trulli" /> <br>
                        <img src="image/logs/raids/{character_id}" alt="Italian Trulli" /> <br>
                        <img src="image/logs/dungs/{character_id}" alt="Italian Trulli" /> <br>
                    </div>                
                </body>
            </html>
        """
