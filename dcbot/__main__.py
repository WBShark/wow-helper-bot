import logging

from dcbot.bot import client
from dcbot.config import config
from dcbot.logs import InterceptHandler

### add retries, timeouts, circuit brekaer

logging.basicConfig(handlers=[InterceptHandler()], level="INFO", force=True)
client.run(config.dc_bot_token, log_handler=None)
