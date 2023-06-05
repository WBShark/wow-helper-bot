import logging

from dpschecker.bot import client
from dpschecker.config import config
from dpschecker.logs import InterceptHandler

### add retries, timeouts, circuit brekaer

logging.basicConfig(handlers=[InterceptHandler()], level="INFO", force=True)
client.run(config.dc_bot_token, log_handler=None)
