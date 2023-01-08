import orjson
from models.common import orjson_dumps
from pydantic import BaseModel, Field, NoneStr


class UserParser(BaseModel):
    id: int = Field(..., alias="twitter_id")
    name: str
    screen_name: str = Field(..., alias="username")
    following_count: int | None = None
    followers_count: int | None = None
    description: NoneStr

    class Config:
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
