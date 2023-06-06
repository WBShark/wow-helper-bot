from dotenv import load_dotenv
from pydantic import BaseSettings, ValidationError


class Config(BaseSettings):
    wlog_id: str = "ID"
    wlog_secret: str = "SECRET"
    grpc_port: str = "50051"


load_dotenv()
try:
    config = Config()
except ValidationError as e:
    raise EnvironmentError("Failed to load config " + str(e.errors())) from e
