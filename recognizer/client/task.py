from typing import Optional

import httpx

from recognizer.schemas import Image


class TaskClient:

    def __init__(self, url: str):
        self.url = url

    def get_task(self) -> Optional[Image]:
        res = httpx.get(f'{self.url}/tasks/')
        if res.status_code == 200:
            image = Image(**res.json())
            return image
        return None
