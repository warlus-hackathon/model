from pathlib import Path

from recognizer.handler.watcher import get_number
from recognizer.schemas import Image


def recognize_image(image: Image) -> Image:
    payload = image.dict()
    filename = payload['name']
    image_path = Path(f'recognizer/file_storage/{filename}')
    payload['obj_number'] = get_number(image_path)
    updated_image = Image(**payload)
    return updated_image
