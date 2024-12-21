from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from db_utils import insert_message, get_messages_by_date, get_messages_by_theme, get_messages_by_theme_and_date
from contracts import MessageCreate

router = APIRouter(tags=["db_service"])

@router.post("/update")
async def update_data(message: MessageCreate, request: Request):
    async with request.state.db as session:
        try:
            message_id = await insert_message(message.dict(), session)
            return JSONResponse(content={"success": True, "message_id": message_id})
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/get_by_date")
async def get_by_date(date: str, request: Request):
    async with request.state.db as session:
        messages = await get_messages_by_date(date, session)
        return JSONResponse(content={"messages": [msg.content for msg in messages]})

@router.get("/get_by_theme")
async def get_by_theme(theme: str, request: Request):
    async with request.state.db as session:
        messages = await get_messages_by_theme(theme, session)
        return JSONResponse(content={"messages": [msg.content for msg in messages]})

@router.get("/get_by_theme_date")
async def get_by_theme_date(theme: str, date: str, request: Request):
    async with request.state.db as session:
        messages = await get_messages_by_theme_and_date(theme, date, session)
        return JSONResponse(content={"messages": [msg.content for msg in messages]})
