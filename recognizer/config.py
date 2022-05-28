import os

from pydantic import BaseModel


class AppConfig(BaseModel):
    endpoint: str


def load_from_env() -> AppConfig:
    endpoint = os.environ['ENDPOINT']
    return AppConfig(
        endpoint=endpoint,
    )


config = load_from_env()
