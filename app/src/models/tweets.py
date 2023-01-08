from typing import List

import orjson
from models.common import orjson_dumps
from pydantic import BaseModel


class Tweets(BaseModel):
    tweet: dict = {}

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
