import logging
import time
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from make_csv import create_csv

logging.basicConfig(level=logging.DEBUG)

logg = logging.getLogger(__name__)

CONFIDENCE = 0.4
SCORE_THRESHOLD = 0.001
IOU_THRESHOLD = 0.001

# конфигурация нейронной сети
config_path = Path('recognizer/handler/model/yolov3.cfg')
# файл весов сети YOLO
weights_path = Path('recognizer/handler/model/warlus.weights')
# файл всех меток классов (объектов)
labels_path = Path('recognizer/handler/model/coco.names')
# файл изображения
image_path = Path('recognizer/file_storage/17.jpg')
filename, ext = image_path.stem, image_path.suffix

# загрузка всех меток классов (объектов)
with open(labels_path, 'r') as f:    
    labels = f.read().strip().split('\n')
    logg.debug(labels)


def image_prepare(image: Path) -> cv2:
    # подготовка изображения
    return cv2.imread(str(image))


def layer_outputs(image: cv2) -> cv2:
    # загружаем сеть YOLO
    # документация https://docs.opencv.org/3.4/d6/d0f/group__dnn.html#gaef8ac647296804e79d463d0e14af8e9d
    net = cv2.dnn.readNetFromDarknet(str(config_path), str(weights_path))
    # прогнозирование
    ####################################################################
    # создать 4D blob
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    logg.debug(f'image.shape: {image.shape}, blob.shape {blob.shape}')
    # усанавливаем blob как вход сети
    net.setInput(blob)
    # получаем имена всех слоев
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
    # прямая связь (вывод) и получение выхода сети
    # измерение времени для обработки в секундах
    return net.forward(ln)


def create_entities(image: cv2, h: int, w: int) -> tuple[list[Any], list[Any], list[Any]]:
    # еребрать выходные данные нейронной сети и отбросить все объекты, уровень достоверности
    # идентификации которых меньше, чем параметр CONFIDENCE
    boxes, confidences, class_ids = [], [], []
    # перебираем каждый выход слоя
    for output in layer_outputs(image):
        # перебираем каждое обнаружение объекта
        for detection in output:
            # извлекаем идентификатор класса (метку) и достоверность (как вероятность)
            # обнаружение текущего объекта
            
            scores = detection[5:]
            
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            #logg.debug(f'detection: {detection}')
            #logg.debug(f'scores: {scores}')
            #logg.debug(f'confidence: {confidence}')
            # отбросьте слабые прогнозы, убедившись, что обнаруженные
            # вероятность больше минимальной вероятности
            if confidence > CONFIDENCE:
                logg.debug(f'detection: {detection}')
                logg.debug(f'scores: {scores}')
                logg.debug(f'confidence: {confidence}')
                # масштабируем координаты ограничивающего прямоугольника относительно
                # размер изображения, учитывая, что YOLO на самом деле
                # возвращает центральные координаты (x, y) ограничивающего
                # поля, за которым следуют ширина и высота поля
                box = detection[:4] * np.array([w, h, w, h])
                logg.debug(f'detection 4: {detection[:4]}')
                logg.debug(f'box: {box}')
                (centerX, centerY, width, height) = box.astype('int')
                # используем центральные координаты (x, y) для получения вершины и
                # и левый угол ограничительной рамки
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # обновить наш список координат ограничивающего прямоугольника, достоверности,
                # и идентификаторы класса
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
            #logg.info(f'detection.shape: {detection.shape}')
    return (boxes, confidences, class_ids)


def render_image(idxs: cv2, image: cv2, boxes, confidences, class_ids) -> None:
    # Отрисовка обнаруженных объектов
    ####################################################################
    # перебираем сохраняемые индексы
    font_scale = 1
    thickness = 2
    point_size = 1

    for i in idxs.flatten():
        # извлекаем координаты ограничивающего прямоугольника
        x, y = boxes[i][0], boxes[i][1]
        w, h = boxes[i][2], boxes[i][3]

        x_2, y_2 = x + w, y + h
        
        x_center = (x + x_2) // 2
        y_center = (y + y_2) // 2

        # рисуем прямоугольник ограничивающей рамки и подписываем на изображении
        color = (0, 255, 0)
        cv2.circle(image, (x_center, y_center), point_size, color, thickness)
        cv2.rectangle(image, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=thickness)
        text = f'{labels[class_ids[i]]}: {confidences[i]:.2f}'
        # вычисляем ширину и высоту текста, чтобы рисовать прозрачные поля в качестве фона текста
        (text_width, text_height) = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, fontScale=font_scale, thickness=thickness,
        )[0]
        text_offset_x = x
        text_offset_y = y - 5
        box_coords = (
            (text_offset_x, text_offset_y),
            (text_offset_x + text_width + 2, text_offset_y - text_height),
        )
        overlay = image.copy()
        cv2.rectangle(overlay, box_coords[0], box_coords[1], color=color, thickness=cv2.FILLED)
        
        # добавим непрозрачность (прозрчость) поля
        image = cv2.addWeighted(overlay, 0.6, image, 0.4, 0)
        # теперь поместим текст (метка,  доверие %)
        cv2.putText(
            image, text, (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=font_scale,
            color=(0, 0, 0),
            thickness=thickness,
        )
        
    new_image_path = f'recognizer/file_storage/{filename}_yolov3{ext}'
    cv2.imwrite(new_image_path, image)


def get_number(image_path: Path) -> int:
    start = time.perf_counter()
    image = image_prepare(image_path)
    # Затем нам нужно нормализовать, масштабировать и изменить это изображение
    height, width = image.shape[:2]
    logg.debug(f'height {height}, width{width}')
    boxes, confidences, class_ids = create_entities(image, height, width)
    # Non-maximal Suppression
    ####################################################################
    # выполнить не максимальное подавление с учетом оценок, определенных ранее
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, SCORE_THRESHOLD, IOU_THRESHOLD)
    index_size = len(idxs)
    if index_size > 0:
        render_image(idxs, image, boxes, confidences, class_ids)
    create_csv(idxs, boxes, image_path.stem)
    delta_time = time.perf_counter() - start
    logg.debug(f'Потребовалось: {delta_time:.2f}s')
    return index_size


#logg.debug(get_number(image_path))
