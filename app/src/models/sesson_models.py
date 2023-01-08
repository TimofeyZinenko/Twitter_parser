from dataclasses import dataclass
from typing import List

import orjson
from models.common import orjson_dumps
from pydantic import BaseModel


class SessonModel(BaseModel):
    session_id: int

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


@dataclass
class Links:
    links: List[str]
