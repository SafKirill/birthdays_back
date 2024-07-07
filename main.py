import uvicorn
import asyncio
import sys
from datetime import datetime, time, timedelta
from typing import Callable

from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.sending_birthdays import get_alert
from api.handlers.userHandlers import user_router
from api.handlers.loginHandlers import login_router
from api.handlers.followHandlers import follow_router
from api.handlers.congratulationHandlers import congratulation_router

sys.setrecursionlimit(500)
#API роуты

#Создание инстанса приложения
app = FastAPI(title="Birthdays")

def schedule_task(func: Callable, exec_time: time):
    async def run_task():
        while True:
            now = datetime.now()
            target_time = datetime.combine(now.date(), exec_time)
            if target_time < now:
                target_time += timedelta(days=1)
            seconds_to_wait = (target_time - now).total_seconds()
            await asyncio.sleep(seconds_to_wait)
            await func()

    asyncio.create_task(run_task())


@app.on_event("startup")
async def startup_event():
    # Запускаем get_alert каждый день в 8:30 утра
    schedule_task(get_alert, time(hour=8, minute=30))

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mainApiRouter = APIRouter()

mainApiRouter.include_router(login_router, tags=["login"])
mainApiRouter.include_router(user_router, tags=["user"])
mainApiRouter.include_router(follow_router, tags=["follow"])
mainApiRouter.include_router(congratulation_router, tags=["congratulation"])

app.include_router(mainApiRouter)
if __name__ == "__main__":
    uvicorn.run(app,host="localhost", port=8000, http="httptools")