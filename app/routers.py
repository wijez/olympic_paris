from fastapi import FastAPI, APIRouter
from app.api import venues_router


def init_router(app: FastAPI):
    main_router = APIRouter()
    main_router.include_router(venues_router)

    app.include_router(main_router)
