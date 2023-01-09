from typing import List

import orjson
from pydantic import BaseModel
from src.models.common import orjson_dumps


class Tweets(BaseModel):
    tweet: dict = {}

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
