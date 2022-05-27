from recognizer.client.api import appclient
from recognizer.schemas import Image


def get_next_task() -> Image:
    return appclient.task.get_task()


def post_answer(updated_image: Image) -> None:
    return appclient.response.put_answer(updated_image)
