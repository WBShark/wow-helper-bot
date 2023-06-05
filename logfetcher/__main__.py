import asyncio
import logging
from dotenv import load_dotenv


import grpc

import logfetcher.proto.log_service_pb2_grpc as log_service_grpc
from logfetcher.servicer import LogFetcherServicer

###add sleep and check


async def serve() -> None:
    server = grpc.aio.server()
    log_service_grpc.add_LogFetcherServicer_to_server(LogFetcherServicer(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":


    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
