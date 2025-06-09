import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.db import async_engine, Base
from src.api.routers import router as auth_router
from src.models.user import User


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield

app = FastAPI()

app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)