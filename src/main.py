import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import lifespan
from api import router as api_router
from api.views import router as views_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(views_router)

@app.get("/")
async def root():
    return {"message": "HiHi ✨!"}

if __name__ == "__main__":
    logger.info("Run app ✨ succesfully ✨")
    uvicorn.run(
        app="main:app",
        reload=True
    )
    