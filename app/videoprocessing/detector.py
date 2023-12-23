import cv2
import os


#from class_detector import Shot
from videoprocessing.class_detector import Shot


def recognize_faces(video_path):
    video = cv2.VideoCapture(video_path)
    shot_count = 0 # счетчик номера кадра
    dir_path = os.path.dirname(os.path.abspath(__file__))    
    datapath = os.getcwd() + r'\dataSet\\'
    spath = dir_path + r'/library/haarcascade_frontalface_default.xml'
    trainpath = os.getcwd() + r'\\trainer\\trainer.yml'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faceCascade = cv2.CascadeClassifier(spath)
    i = 0 # счетчик сделанных фото неопознанных лиц

    try:
        recognizer.read(trainpath)
    except Exception as e:
        print(e)
    while True:
        # получаем видеопоток
        try:
            ret, shot_ =video.read()
        except Exception as e:
            print(e)

        if ret:
            shot = Shot(shot_)
            shot_count += 1 
        else:
            shot.train(recognizer, faceCascade, datapath, trainpath)
            break
        # определяем лица на видео
        faces = shot.detect_faces(faceCascade)
        # перебираем все найденные лица
        for(x,y,w,h) in faces:
            i = shot.recognize_face((x,y,w,h), faceCascade, recognizer, i, 80, datapath, trainpath)
        yield shot_count

if __name__ == '__main__':
    recognize_faces("video_2023-09-26_17-46-35.mp4")
    cv2.destroyAllWindows()