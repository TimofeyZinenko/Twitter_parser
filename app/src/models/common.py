import orjson
from core.config import config_settings


def orjson_dumps(v, *, default):
    """rjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем."""
    return orjson.dumps(v, default=default).decode()


def get_whole_list():
    with open(config_settings.base_dir + "/tests/data.txt", "r") as f:
        full_list = f.readlines()
        return list(map(lambda x: x.strip(), full_list))
