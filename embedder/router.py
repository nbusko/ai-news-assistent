from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from embedder import Embedder
from contracts import UserRequest


router = APIRouter(tags=["embedder"])
embedder = Embedder()


@router.post("/search")
async def search(texts : UserRequest):
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=embedder.answer(texts.texts)
    )