from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.database import db_helper, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()