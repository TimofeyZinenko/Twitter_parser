from logging import config as logging_config

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from src.api.v1 import session_details, sessons, tweets, user_info
from src.core.config import config_settings
from src.db import redis_cache

logging_config.dictConfig(config_settings.logger_config)


app = FastAPI(
    title=config_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pool = aioredis.ConnectionPool.from_url(
        config_settings.redis_dsn, max_connections=20
    )
    retry = Retry(ExponentialBackoff(), 6)
    redis_cache.redis_cache = aioredis.Redis(
        connection_pool=pool,
        decode_responses=True,
        retry=retry,
        retry_on_timeout=True,
    )


@app.on_event("shutdown")
async def shutdown():
    await redis_cache.redis_cache.close()
    await redis_cache.redis_cache.connection_pool.disconnect()


app.include_router(sessons.router, prefix="/api/v1", tags=["list parsing"])
app.include_router(
    session_details.router, prefix="/api/v1", tags=["parsed list status"]
)
app.include_router(user_info.router, prefix="/api/v1", tags=["User information"])
app.include_router(tweets.router, prefix="/api/v1", tags=["Tweets"])

if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
