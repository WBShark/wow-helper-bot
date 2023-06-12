import asyncio
import logging

import grpc # type: ignore
from logfetcher.config import config

import logfetcher.proto.log_service_pb2_grpc as log_service_grpc
from logfetcher.servicer import LogFetcherServicer

###add sleep and check


async def serve() -> None:
    grpc_server: grpc.aio.Server = grpc.aio.server()
    log_service_grpc.add_LogFetcherServicer_to_server(LogFetcherServicer(), grpc_server)
    grpc_server.add_insecure_port(":".join(["[::]", config.grpc_port]))
    await grpc_server.start()
    await grpc_server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
