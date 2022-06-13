from pathlib import Path

from recognizer.handler.yolov5 import detect


model = 'recognizer/handler/yolov5/models/best.pt'
image = Path('recognizer/file_storage/17.jpg')


def get_number(image_path: Path = image) -> int:
    detect.run(weights=model, source=str(image_path), nosave=True, save_txt=True, save_conf=True)
    return 3

get_number()
