from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.routers import init_router

import aioredis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)


@app.get("/")
async def hello_word():
    return "Olympic Paris 2024"


# @app.on_event("startup")
# async def startup_event():
#     global r
#     r = await aioredis.create_redis_pool(
#         "redis://:UILbGhJkmQyfQ4i0N5Fobftd5fkPObib@redis-12662.c263.us-east-1-2.ec2.redns.redis-cloud.com:12662",
#         encoding="utf-8"
#     )
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     r.close()
#     await r.wait_closed()


init_router(app)
