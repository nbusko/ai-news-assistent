from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

# from contracts import UserRequest
from embedder import Embedder


router = APIRouter(tags=["embedder"])
embedder = Embedder()


@router.get("/search")
async def search(text: str):
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=embedder.answer(text)
    )