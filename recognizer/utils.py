from recognizer.schemas import Image


def update_image_field(image: Image, field: str, new_value) -> Image:
    payload = image.dict()
    payload[field] = new_value
    updated_image = Image(**payload)
    return updated_image
