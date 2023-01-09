from typing import List

import orjson
from pydantic import BaseModel, dataclasses
from src.models.common import orjson_dumps


@dataclasses.dataclass
class SessonDetails:
    username: str
    status: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
