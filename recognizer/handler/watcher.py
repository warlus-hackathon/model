from pathlib import Path
import shutil

import cv2
from PIL import Image

from recognizer.handler.yolov5 import detect

model = 'recognizer/handler/yolov5/models/warlus.pt'
file_storage = 'recognizer/file_storage'


def read_labels(labels: Path) -> list[list[str]]:
    with open(labels, 'r') as label:
        coord = label.readlines()

    boxes = []
    for box in coord:
        box = box.replace('\n', '')
        box_list = box.split()
        boxes.append(box_list)

    labels_dir = labels.parent
    shutil.copy(labels, labels_dir.parent / labels.name)
    shutil.rmtree(labels_dir, ignore_errors=True)

    return boxes


def write_image(image_path: Path, boxes: list):
    image = cv2.imread(str(image_path))
    height, width, _ = image.shape

    for box in boxes:
        x = int(float(box[1]) * width)
        y = int(float(box[2]) * height)
        cv2.circle(image, (x, y), 3, (0, 255, 0), 4)

    msg = f'Warlus number = {len(boxes)}'
    cv2.putText(image, msg, (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 10, cv2.LINE_AA)
    new_image = Path(image_path.parent, f'{image_path.stem}_yolov3{image_path.suffix}')
    cv2.imwrite(new_image, image)


def get_number(image_path: Path) -> int:
    im = Image.open(str(image_path))
    detect.run(
        weights=model,
        source=str(image_path),
        imgsz=im.size,
        nosave=True,
        save_txt=True,
        save_conf=True,
        project=file_storage,
    )
    labels = Path(file_storage, 'exp', f'{image_path.stem}.txt')
    boxes = read_labels(labels)
    write_image(image_path, boxes)
    return len(boxes)
