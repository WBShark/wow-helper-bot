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
            logging.warning(f"Crawl outadated at {datetime.now()}")
            await crawler.crawl()
            logging.warning(f"Crawled at {datetime.now()}")
        if crawler.guild_outdated():
            logging.warning(f"Updating guilds at {datetime.now()}")
            await crawler.update_guilds()
            logging.warning(f"Guilde updated at {datetime.now()}")
        if crawler.rio_scores_outdated():
            logging.warning(f"Updating rio score at {datetime.now()}")
            await crawler.update_character_scores()
            logging.warning(f"Updated rio score at {datetime.now()}")
        if crawler.shout_outdated():
            logging.warning(f"Shouting at {datetime.now()}")
            await crawler.shout()
            logging.warning(f"Shoueted at {datetime.now()}")
        logging.warning(f"Crawl ended {datetime.now()}")
        time.sleep(500)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(updater())
