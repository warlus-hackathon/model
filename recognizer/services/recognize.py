from recognizer.handler.recognizer import run
from recognizer.schemas import Image


def recognize_image(image: Image) -> Image:
    payload = image.dict()
    payload['obj_number'] = len(payload['name'])
    updated_image = Image(**payload)
    return updated_image
