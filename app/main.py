from threading import Thread
from fastapi import FastAPI
import uvicorn

from api.worker import router

# Создание объекта приложения. Запуск uvicorn main:app, uvicorn main:app --reload
app = FastAPI()

app.include_router(router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

