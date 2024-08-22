import json
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client as r
from pydantic import BaseModel


async def validate_and_update_cache(
        cache_key: str,
        db_data: BaseModel,
        ttl: int = 3600
):
    cached_data = await r.get(cache_key)
    db_data_dict = db_data.dict()

    if cached_data:
        cached_data_dict = json.loads(cached_data)
        if cached_data_dict == db_data_dict:
            return cached_data_dict
        else:
            await r.setex(cache_key, ttl, json.dumps(db_data_dict))
            return db_data_dict

    await r.setex(cache_key, ttl, json.dumps(db_data_dict))
    return db_data_dict
