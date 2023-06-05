import httpx
from pydantic import HttpUrl, parse_obj_as
from requests_html import AsyncHTMLSession, HTMLResponse

from logfetcher.cruds.processros import find_character_id
from logfetcher.models.characters import Character, CharacterCreate


async def render_page(rio_url: HttpUrl) -> HTMLResponse:
    RIOsession: AsyncHTMLSession = AsyncHTMLSession()
    rio_page: HTMLResponse = await RIOsession.get(rio_url)

    await rio_page.html.arender(timeout=5000)

    return rio_page


async def get_wlog_link(rio_page: HTMLResponse) -> str:
    link: str
    for link in rio_page.html.links:
        if "warcraftlog" in link:
            return parse_obj_as(HttpUrl, link)


def get_character_id(rio_page: HTMLResponse) -> int:
    return int(find_character_id(rio_page.html.text))


async def create_character(char: CharacterCreate) -> str:
    rio_page: HTMLResponse = await render_page(char.rio_url)
    wlog_url: HttpUrl = await get_wlog_link(rio_page)
    wlog_info: list[str] = wlog_url.split("/")

    rio_info: list[str] = str(char.rio_url).split("/")
    rio_id: int = get_character_id(rio_page)

    return Character(
        rio_url=char.rio_url,
        rioid=rio_id,
        wlog_url=wlog_url,
        wlog_server=wlog_info[-2],
        rio_server=rio_info[-2],
        name=wlog_info[-1],
        server_region=wlog_info[-3],
    )

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
