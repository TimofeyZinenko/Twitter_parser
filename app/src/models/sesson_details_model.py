from typing import List

import orjson
from models.common import orjson_dumps
from pydantic import BaseModel, dataclasses


@dataclasses.dataclass
class SessonDetails:
    username: str
    status: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps