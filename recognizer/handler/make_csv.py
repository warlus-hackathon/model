import csv
import logging

logger = logging.getLogger(__name__)


def write_csv(boxes: list[str], file_name: str):
    csv_file = f'recognizer/file_storage/{file_name}.csv'

    with open(csv_file, 'w', newline='') as myfile:
        wr = csv.writer(myfile, delimiter='\n', quoting=csv.QUOTE_ALL)
        wr.writerow([f'{file_name}.csv'])
        wr.writerow(boxes)


def create_csv(idxs, boxes, file_name: str):
    centers = []
    for i in idxs.flatten():
        # извлекаем координаты ограничивающего прямоугольника
        x_1, y_1 = boxes[i][0], boxes[i][1]
        w, h = boxes[i][2], boxes[i][3]
        x_2, y_2 = x_1 + w, y_1 + h
        
        x_center = (x_1 + x_2) // 2
        y_center = (y_1 + y_2) // 2
        #msg = f'x: {x_1} y: {y_1} w: {w} h: {h} x2: {x_2} y2: {y_2}\n center: ({x_center}, {y_center})'
        centers.append(f'{x_center},{y_center}')
        #logger.debug(msg)
    write_csv(centers, file_name)
    logger.debug(centers)
