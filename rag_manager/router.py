from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from contracts import RequestData
import logging

from request_manager import RequestManager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["rag_manager"])

@router.post("/answer")
async def response(data: RequestData):
    logger.info(f"Received request: {data.query}")
    manager = RequestManager()
    try:
        answer = await manager.get_full_answer(data.query)
        logger.info(f"Returning answer: {answer}")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"answer": answer}
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate")
async def response(data: RequestData):
    logger.info(f"Received request: {data.query}")
    manager = RequestManager()
    try:
        answer = await manager.get_faiss_answer(data.query)
        logger.info(f"Returning answer: {answer}")
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=answer
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
