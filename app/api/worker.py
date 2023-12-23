import asyncio, aiofiles
import os
from http import HTTPStatus
from fastapi import APIRouter, BackgroundTasks, UploadFile, FastAPI, File
import functools
from typing import Dict, List
from uuid import UUID, uuid4
import uvicorn
from concurrent.futures import ProcessPoolExecutor
from pydantic import BaseModel, Field
import cv2

from videoprocessing.detector import recognize_faces
import multiprocessing as mp




executor = ProcessPoolExecutor()
loop = asyncio.get_event_loop()

router = APIRouter()

async def video_validator(filename):
    """Проверка файла на ошибки."""
    try:
        vid = cv2.VideoCapture(filename)
        if not vid.isOpened():
            raise NameError('Just a Dummy Exception, write your own')
    except cv2.error as e:
        print("cv2.error:", e)
        return False
    except Exception as e:
        print("Exception:", e)
        return False
    
    print("no problem reported")
    return True

class Job(BaseModel):
    uid: UUID = Field(default_factory=uuid4)
    status: str = "in_progress"
    progress: int = 0
    result: int = None



jobs: Dict[UUID, Job] = {}  # Dict as job storage
queue = mp.SimpleQueue()

def test_queue(n):
    print(n)
    for i in range(1,n):
        yield i

def init_queue(queue):
    globals()['queue'] = queue


def wrapper(x):
    q = queue
    for item in test_queue(x):
        q.put(item)

async def long_task(queue: asyncio.Queue, frame_count: int, video_path: str):
    #for i in recognize_faces(video_path):  # do work and return our progress
    #task = asyncio.create_task(test_queue(10))
    print('long_task begin')
    coro = asyncio.to_thread(test_queue())
    # планирование задачи
    task = asyncio.create_task(coro)
        
    while i := await asyncio.gather(task):
        per_cent = i
        print(f"DONE {per_cent}")
    #for i in test_queue(10):
        #per_cent = i * 100 / frame_count
        print(per_cent)
        await queue.put(per_cent)
    await queue.put(None)


async def start_new_task(
    background_tasks: BackgroundTasks, uid: UUID, frame_count: int, video_path: str) -> None:
    #queue = asyncio.Queue()
    print('Begin')
    POISON = 'POISON'

    with mp.Pool(processes=4, initializer=init_queue, initargs=(queue,)) as pool:
        pool.map_async(
            func=wrapper,
            #iterable=range(0, 100, 10),
            chunksize=1,
            callback=lambda _: queue.put(POISON)
        )
        for res in iter(queue.get, POISON):
            print(res)

    print('>>>>Begin')
    
    jobs[uid].status = "complete"


@router.post("/new_task", status_code=HTTPStatus.ACCEPTED)
async def task_handler(    
    background_tasks: BackgroundTasks, video_file: UploadFile = File(...),
):
    file_location = os.path.join('./', os.path.basename(video_file.filename))
    async with aiofiles.open(file_location, "wb+") as file_object:
        while chunk := await video_file.read(1024 * 1024): # = 1MB
            await file_object.write(chunk) 
    await video_file.close()
    if not await video_validator(file_location):
        return {"info": f"Файл '{video_file.filename}' поврежден или не является видеофайлом."}
    new_task = Job()
    jobs[new_task.uid] = new_task
    cap = cv2.VideoCapture(file_location) # количество кадров в видео
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    background_tasks.add_task(start_new_task, background_tasks, new_task.uid, frame_count, file_location)
    #background_tasks.add_task(start_new_task)
    return new_task


@router.get("/task/{uid}/status")
async def status_handler(uid: UUID):
    return jobs[uid]


if __name__ == '__main__':
    # Команда на запуск uvicorn.
    # Здесь же можно указать хост и/или порт при необходимости,
    # а также другие параметры.
    uvicorn.run('worker:router', reload=True)