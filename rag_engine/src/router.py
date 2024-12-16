from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from src.dao import update_rag, search_by_embedding, get_text_embedding
from src.contracts import RAGContent, RetrieveContent
from src.config import faiss_func
# from dao import update_rag, search_by_embedding, get_text_embedding
# from contracts import RAGContent, RetrieveContent
# from config import faiss_func

router = APIRouter(prefix="/api/v1", tags=["rag_api"])


@router.post("/update")
async def search(
    request: Request,
    rag_content: RAGContent,
):
    """ """
    await update_rag(
        rag_content=rag_content.model_dump(),
        session=request.state.db,
        f_index=request.state.fd,
    )

    return JSONResponse(content={"success": True})


@router.post("/retrieve")
async def search(
    request: Request,
    retrieve_content: RetrieveContent,
):
    """ """
    data = retrieve_content.model_dump()
    emb = await get_text_embedding(text=faiss_func(data))

    result = await search_by_embedding(
        embedding=emb,
        topn=data["topn"],
        session=request.state.db,
        f_index=request.state.fd,
    )

    return JSONResponse(content={"result": result, "success": True})
