import logging
import sys
import typing

from google.protobuf.internal.containers import MessageMap
from loguru import logger
from pydantic import BaseModel

from logfetcher.proto.log_service_pb2 import BossResponse


class InterceptHandler(logging.Handler):
    @typing.no_type_check
    def emit(self, record) -> None:
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class LogInfo(BaseModel):
    rankings: list[int]
    name: str


class RaidLogInfo(BaseModel):
    rankings: MessageMap[str, BossResponse]
    name: str
