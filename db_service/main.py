import logging
from contextlib import asynccontextmanager
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import database
from router import router
from db_utils import insert_data_from_csv_if_empty

@asynccontextmanager
async def init_tables(app: FastAPI):
    try:
        async with database.engine.begin() as conn:
            await conn.run_sync(database.Base.metadata.create_all)
        app.state.Logger.info("Tables created successfully.")       
    except Exception as e:
        app.state.Logger.error(f"Error creating tables: {e}")
    yield


app = FastAPI(
    title="db_service", 
    version="0.0.1",
    docs_url="/docs",
    redoc_url=None,
    lifespan=init_tables,
)

app.state.Logger = logging.getLogger(name="db_service")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
app.state.Logger.addHandler(handler)
app.state.Logger.setLevel("DEBUG")

app.include_router(router)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = database.async_session_maker()
    
    async with request.state.db as session:
        messages = await insert_data_from_csv_if_empty(os.getenv("CSV_PATH"), session)
        
    try:
        response = await call_next(request)
    except Exception as exc:
        detail = getattr(exc, "detail", None)
        unexpected_error = not detail
        if unexpected_error:
            args = getattr(exc, "args", None)
            detail = args[0] if args else str(exc)
        app.state.Logger.error(detail, exc_info=unexpected_error)
        status_code = getattr(exc, "status_code", 500)
        response = JSONResponse(
            content={"detail": str(detail), "success": False}, status_code=status_code
        )
    finally:
        await request.state.db.close()

    return response


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8020,
    )