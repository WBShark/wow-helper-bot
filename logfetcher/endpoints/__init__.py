from fastapi import APIRouter

from .characters import characters_router
from .ranks import ranks_router

root_router: APIRouter = APIRouter()

root_router.include_router(characters_router, prefix="/characters")
root_router.include_router(ranks_router, prefix="/ranks")
