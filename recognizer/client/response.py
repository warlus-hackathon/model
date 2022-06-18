import httpx

from recognizer.schemas import Image


class ResponseClient:

    def __init__(self, url: str):
        self.url = url

    def put_answer(self, image: Image) -> None:
        image_id = image.dict()['uid']
        headers = {"Content-Type": "application/json"}
        data = image.json()
        res = httpx.put(
            f'{self.url}/images/{image_id}', data=data, headers=headers,  # type: ignore
        )
        res.raise_for_status()
