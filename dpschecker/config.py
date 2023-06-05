from pydantic import BaseSettings, ValidationError
from dotenv import load_dotenv

class Config(BaseSettings):
    dc_bot_token: str = "DC_BOT_TOKEN"

load_dotenv()
try:
    config = Config()
except ValidationError as e:
    raise EnvironmentError("Failed to load config " + str(e.errors())) from e
