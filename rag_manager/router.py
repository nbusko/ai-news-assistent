from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from contracts import 
from request_manager import RequestManager


router = APIRouter(tags=["manager"])
manager = RequestManager()


@router.post("/get")
async def responce(data: str):
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"answer": manager.get(data)}
    )