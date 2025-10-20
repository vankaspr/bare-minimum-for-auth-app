import uvicorn
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "HiHi ✨!"}

if __name__ == "__main__":
    logger.info("Run app ✨ succesfully ✨")
    uvicorn.run(
        app="main:app",
        reload=True
    )
    