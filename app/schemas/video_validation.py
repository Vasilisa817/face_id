import asyncio
import sys
import cv2


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

if __name__ == '__main__':
   asyncio.run(video_validator("requirements.txt"))