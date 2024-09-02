import httpx
from fastapi import HTTPException,  Request
from time import time
rate_limit_storage = {}


async def get_httpx_client():
    async with httpx.AsyncClient() as client:
        yield client


def rate_limit(request: Request, limit: int = 5, period: int = 60):
    client_ip = request.client.host
    current_time = time()

    requests = rate_limit_storage.get(client_ip, [])

    requests = [req for req in requests if req > current_time - period]

    rate_limit_storage[client_ip] = requests

    if len(requests) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Add the current request time to the list
    rate_limit_storage[client_ip].append(current_time)
