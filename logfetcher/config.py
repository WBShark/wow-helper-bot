from pydantic import BaseSettings, ValidationError

ONE_HOUR: int = 3600


class Config(BaseSettings):
    wlog_id: str = "ID"
    wlog_secret: str = "SECRET"
    grpc_port: str = "50051"
    dc_bot_token: str = "DC_BOT_TOKEN"


try:
    config = Config()
except ValidationError as e:
    raise EnvironmentError("Failed to load config " + str(e.errors())) from e
