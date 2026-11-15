from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.db import Base, engine
from src.user.router import user_route
from src.pregnancy.router import pregnancy_router
from src.logs.router import logs_router
from src.auth.router import auth_router
from src.utils.redis import create_redis
import redis.asyncio as redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    app.state.redis = await create_redis()

    try:
        yield
    finally:
        await app.state.redis.aclose()
        await engine.dispose()

app = FastAPI(title="Her-Flowmate", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route)
app.include_router(auth_router)
app.include_router(pregnancy_router)
app.include_router(logs_router)







