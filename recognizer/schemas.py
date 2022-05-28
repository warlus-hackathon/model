from pydantic import BaseModel


class Image(BaseModel):
    uid: int
    name: str
    path: str
    obj_number: int
    was_recognized: int
