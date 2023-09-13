import json
import logging

import httpx
import js2py
from bs4 import BeautifulSoup, ResultSet
from pydantic import HttpUrl

from logfetcher.models.characters import Character, CharacterCreate, CharacterRioData

js_script = """
function Immitate_Wlog_link() {
    var e=this_is_region;
    var t=this_is_realm;
    var n=this_is_name;
    var r = t.slug;
    return -1 !== ["ru_RU", "zh_TW", "zh_CN", "ko_KR"].indexOf(t.locale) && (r = (r = t.altSlug).replace(/й/g, "и")),
    "https://www.warcraftlogs.com/character/".concat(e, "/").concat(r, "/").concat(n)
}
Immitate_Wlog_link()
"""


async def get_wlog_link(region: str, realm: str, name: str) -> HttpUrl:
    js = js_script.replace("this_is_region", "'" + region + "'")
    js = js.replace("this_is_realm", realm.replace("'", '"'))
    js = js.replace("this_is_name", "'" + name + "'")
    return js2py.eval_js(js)


async def get_rio_initial_data(rio_url: HttpUrl) -> dict:
    async with httpx.AsyncClient() as client:
        rio_page: httpx.Response = await client.get(rio_url, timeout=1000)
    link: ResultSet
    soup = BeautifulSoup(rio_page.text, "html.parser")
    for link in soup.find_all("script"):
        if link.string and "window.__RIO_INITIAL_DATA" in link.string:
            return json.loads(
                link.string[link.string.find("{") : link.string.find(";")]
            )


async def create_character(character: CharacterCreate) -> Character:
    logging.warning(f"Parsing character {character.rio_url}")
    try:
        character_json_data: CharacterRioData = CharacterRioData.parse_obj(
            await get_rio_initial_data(character.rio_url)
        )
        wlog_url: HttpUrl = await get_wlog_link(
            character_json_data.characterDetails.character.region["slug"],
            str(dict(character_json_data.characterDetails.character.realm)),
            character_json_data.characterDetails.character.name,
        )
        wlog_info: list[str] = wlog_url.split("/")

        rio_info: list[str] = str(character.rio_url).split("/")
        rio_id: int = int(character_json_data.characterDetails.character.id)

        return Character(
            rio_url=character.rio_url,
            rio_id=rio_id,
            wid=None,
            wlog_url=wlog_url,
            wlog_server=wlog_info[-2],
            rio_server=rio_info[-2],
            name=wlog_info[-1],
            server_region=wlog_info[-3],
            realm_id=character_json_data.characterDetails.character.realm.id,
            realm_name=character_json_data.characterDetails.character.realm.name,
        )
    except Exception:
        logging.error(f"Failed to process character {character.rio_url}")
        raise ValueError


"""
async def fetch_logs(character: Character):
    try:
        with httpx.Client() as client:
            result = client.get('https://raider.io/api/characters/' + character.server_region + "/" +
                                character.en_server + "/" + character.name,
                                params={"season" : "season-df-1"})
            print(result.text)
    except Exception as e:
        print(e.with_traceback())
        print(f"Error while log fetching")
    return 1"""
