import os
import cv2
from PIL import Image
import numpy as np


class Shot():

    def __init__(self, shot) -> None:
        self.shot = cv2.cvtColor(shot, cv2.COLOR_BGR2GRAY)
    
    def detect_faces(self, faceCascade):
        faces=faceCascade.detectMultiScale(
            self.shot,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces    
        
    def train(self, recognizer, faceCascade, datapath, trainpath):
        image_paths = [os.path.join(datapath, f) for f in os.listdir(datapath)]
        # списки картинок и подписей на старте пустые
        images = []
        labels = []
        # перебираем все картинки в датасете 
        for image_path in image_paths:
            # читаем картинку и сразу переводим в ч/б
            image_pil = Image.open(image_path).convert('L')
            # переводим картинку в numpy-массив
            image = np.array(image_pil, 'uint8')
            # получаем id пользователя из имени файла
            nbr = int(os.path.split(image_path)[1].split("_")[0])

            # определяем лицо на картинке
            faces = faceCascade.detectMultiScale(image)
            # если лицо найдено
            for (x, y, w, h) in faces:
                # добавляем его к списку картинок 
                images.append(image[y: y + h, x: x + w])
                # добавляем id пользователя в список подписей
                labels.append(nbr)
                # выводим текущую картинку на экран
                cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
                cv2.waitKey(100)
        
        recognizer.train(images, np.array(labels))
        # сохраняем модель
        recognizer.save(trainpath)
        cv2.destroyAllWindows()
    
    def recognize_face(self, params, faceCascade, recognizer, i, name, datapath, trainpath):        
        # получаем id пользователя
        (x,y,w,h) = params
        id, coord = recognizer.predict(self.shot[y:y+h,x:x+w])
        font = cv2.FONT_HERSHEY_SIMPLEX
        if coord >= 110:                
            if i == 3:
                name += 1 # меняем имя для следующего лица
                self.train(recognizer, faceCascade, datapath, trainpath)
                i = 0
            else:                
                if self.write_plot(datapath, name, i, params):
                    i += 1 # если фото записано, счетчик увеличиваем
                    
        else:
            # рисуем прямоугольник вокруг лица
            cv2.rectangle(self.shot,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
            cv2.putText(self.shot, str(id) + ', ' + str(coord), (x,y+h), font, 1.1, (0,255,0))
            # выводим окно с изображением с камеры
            cv2.imshow('Face recognition',self.shot)
            # делаем паузу
            cv2.waitKey(100)
        return i
    
    def write_plot(self, datapath, name, i, params):
        offset = 50
        (x,y,w,h) = params
        height, width = self.shot.shape
        y_down = y-offset if y-offset > 0 else 0
        y_up = y+h+offset if y+h+offset < height else height
        x_down = x-offset if x-offset > 0 else 0
        x_up = x+w+offset if x+w+offset < width else width
        try:
            cv2.imwrite(
                datapath + str(name) + '_' + str(i) + '.jpg',
                self.shot[y_down:y_up,x_down:x_up]
            )
            return True
        except Exception as e:
            print('imwrite: ', e)
            return False
