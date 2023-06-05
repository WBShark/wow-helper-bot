from pydantic import BaseSettings, ValidationError
from dotenv import load_dotenv

class Config(BaseSettings):
    wlog_id: str = "ID"
    wlog_secret: str = "SECRET"

load_dotenv()
try:
    config = Config()
except ValidationError as e:
    raise EnvironmentError("Failed to load config " + str(e.errors())) from e
