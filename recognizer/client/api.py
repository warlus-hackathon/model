from recognizer.client.response import ResponseClient
from recognizer.client.task import TaskClient
from recognizer.config import config


class AppClient:

    def __init__(self, endpoint: str) -> None:
        self.task = TaskClient(endpoint)
        self.response = ResponseClient(endpoint)


appclient = AppClient(config.endpoint)
