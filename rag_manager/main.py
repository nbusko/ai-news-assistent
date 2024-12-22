import uvicorn
from fastapi import FastAPI
import logging
from logging_config import setup_logging

from router import router as root_router

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rag Manager",
    description="Receive request from bot and front and return final result",
    version="0.0.1",
    docs_url="/docs",
    redoc_url=None,
)

app.include_router(root_router)

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8010)
