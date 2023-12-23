import os
import shutil
import aiofiles
from fastapi import APIRouter, UploadFile, File
from schemas.video_validation import video_validator
from multiprocessing import Process


from worker import worker


router = APIRouter()


@router.get(
    '/',
    tags=['common methods',],
    summary='Описание сервиса'
)
async def main():
    """Показать описание сервиса."""
    return {'Hello': 'FastAPI'}


@router.get(
    '/list',
    tags=['common methods',],
    summary='Вывести список всех загруженных видео'
)
async def list_video():
    """Вывести список всех загруженных видео."""
    return


@router.get(
    '/video/{video_id}',
    tags=['special methods',],
    summary='Показать статус и информацию по видео'
)
async def get_video(video_id: int) -> dict[str, str]:
    """
    Получение списка загруженных видео (включая текущий статус, прогресс
    выполнения и результат обработки).
    
    - **video_id**: номер id видео
    """
    return


@router.post(
    '/video',
    tags=['common methods',],
    summary='Загрузить видео'
)
async def post_video(
    video_file: UploadFile = File(...)
):
    """Загрузка и обработка видео-файлов."""

    file_location = os.path.join('./', os.path.basename(video_file.filename))
    async with aiofiles.open(file_location, "wb+") as file_object:
        while chunk := await video_file.read(1024 * 1024): # = 1MB
                await file_object.write(chunk) 
    await video_file.close()
    if not await video_validator(file_location):
        return {"info": f"Файл '{video_file.filename}' поврежден или не является видеофайлом."}

    return {"info": f"Файл '{video_file.filename}' сохранен как '{file_location}'"}


@router.post(
    '/video/{video_id}',
    tags=['special methods',],
    summary='Остановка/отмена обработки выбранного видео'
)
async def update_video(video_id: int) -> dict[str, str]:
    """
    Остановка/отмена обработки выбранного видео.
    
    - **video_id**: номер id видео
    """
    return
