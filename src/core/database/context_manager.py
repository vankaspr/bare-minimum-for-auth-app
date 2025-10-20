from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # await conn.run_sync(Base.metadata.drop_all)
    yield
    # shutdown
    await db_helper.dispose()