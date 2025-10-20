import uvicorn
import logging
from fastapi import FastAPI
from core.database import lifespan

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "HiHi ✨!"}

if __name__ == "__main__":
    logger.info("Run app ✨ succesfully ✨")
    uvicorn.run(
        app="main:app",
        reload=True
    )
    