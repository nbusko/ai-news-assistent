from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

from contracts import WorkerRequest
from neural_worker import Worker


router = APIRouter(tags=["worker"])
worker = Worker()


@router.post("/generate")
async def responce(data: WorkerRequest):
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"answer": worker.answer(data)}
    )

