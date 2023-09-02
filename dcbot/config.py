from pydantic import BaseSettings, ValidationError


class Config(BaseSettings):
    dc_bot_token: str = "DC_BOT_TOKEN"
    grpc_port: str = "50051"


try:
    config = Config()
except ValidationError as e:
    raise EnvironmentError("Failed to load config " + str(e.errors())) from e
