from litestar import Litestar
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig

from logapp.routes import character_router

logging_config = LoggingConfig(
    loggers={
        "my_app": {
            "level": "INFO",
            "handlers": ["queue_listener"],
        }
    }
)

app: Litestar = Litestar(
    route_handlers=[character_router],
    openapi_config=OpenAPIConfig(title="My API", version="1.0.0"),
    logging_config=logging_config,
)
