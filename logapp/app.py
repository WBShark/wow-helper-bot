from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from loguru import logger

from logapp.routes import character_router

app: Litestar = Litestar(
    route_handlers=[character_router],
    openapi_config=OpenAPIConfig(title="My API", version="1.0.0"),
)
