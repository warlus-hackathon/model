from pathlib import Path

from PIL import Image

from recognizer.handler.yolov5 import detect


model = 'recognizer/handler/yolov5/models/best.pt'
image = Path('recognizer/file_storage/17.jpg')
file_storage = 'recognizer/file_storage'


def read_labels():
    pass


def get_number(image_path: Path = image) -> int:     
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

    return 3

get_number()
