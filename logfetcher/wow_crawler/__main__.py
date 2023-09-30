import asyncio
import logging
import time
from datetime import datetime

from logfetcher.wow_crawler.crawler import WoWCrawler


async def updater() -> None:
    crawler: WoWCrawler = WoWCrawler(time.time())
    await crawler.initial_actions()

    while True:
        logging.warning(f"Initializing crawl at {datetime.now()}")
        if crawler.crawl_outdated():
            try:
                logging.warning(f"Crawl outadated at {datetime.now()}")
                await crawler.crawl()
                logging.warning(f"Crawled at {datetime.now()}")
            except Exception as e:
                logging.error(e)
                logging.error("Crawl failed")
        if crawler.guild_outdated():
            try:
                logging.warning(f"Updating guilds at {datetime.now()}")
                await crawler.update_guilds()
                logging.warning(f"Guilde updated at {datetime.now()}")
            except Exception as e:
                logging.error("Guilds update failed")
                logging.error(e)
        if crawler.rio_scores_outdated():
            try:
                logging.warning(f"Updating rio score at {datetime.now()}")
                await crawler.update_character_info()
                logging.warning(f"Updated rio score at {datetime.now()}")
            except Exception as e:
                logging.error(e)
                logging.error("Rio update failed")
        if crawler.shout_outdated():
            try:
                logging.warning(f"Shouting at {datetime.now()}")
                await crawler.shout()
                logging.warning(f"Shoueted at {datetime.now()}")
            except Exception as e:
                logging.error(e)
                logging.error("Shout failed")
        logging.warning(f"Crawl ended {datetime.now()}")
        time.sleep(1000)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(updater())
