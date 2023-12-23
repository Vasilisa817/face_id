from pathlib import Path


# путь к датасету с фотографиями пользователей
dataPath =Path('../dataSet')
# путь к примитивам Хаара
spath = Path('app/../haarcascade_frontalface_default.xml')

print((dataPath), (spath))
