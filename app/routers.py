from fastapi import FastAPI, APIRouter
from app.api import venues_router, events_router, auth_router, competitors_router


def init_router(app: FastAPI):
    main_router = APIRouter()
    main_router.include_router(venues_router)
    main_router.include_router(events_router)
    main_router.include_router(auth_router)
    main_router.include_router(competitors_router)

    app.include_router(main_router)
