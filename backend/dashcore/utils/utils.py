import collections.abc
import datetime
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path

import requests
import yaml

from dashcore.DBConnectors.RedisConnector import RedisConnector
from dashcore.services.Exception import CustomException
from dashcore.services.ExceptionCode import ExceptionCode
from dashcore.services.ExceptionMessage import ExceptionMessage
from dashcore.services.bashcore_config import Config


def date_converter(date: str):
    date = date + " " + str(datetime.today().year)
    return datetime.strptime(date, '%A %b %d %Y').date().isoformat()


def event_impact_convertor(event_type: list) -> int:
    if "star" in event_type:
        return 1
    elif "djstar" in event_type:
        return 2
    elif "bullet" in event_type:
        return 3
    else:
        return 4


def get_html_text(url):
    try:
        result = requests.get(url).text
    except Exception:
        raise CustomException(code=ExceptionCode.BAD_REQUEST,
                              message=ExceptionMessage.DASHCORE_URL_INVALID)
    return result


def load_yml(file):
    file = Path(file)
    try:
        with file.open() as f:
            d = yaml.full_load(f)
            if d is None:
                d = dict()
    except (FileNotFoundError, JSONDecodeError):
        d = dict()
    return d


def update_nested_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_nested_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def get_config() -> Config:
    source_config = load_yml(Path(__file__).parent / '..' / 'config.yml')
    local_source_config = load_yml(Path(__file__).parent / '..' / 'config-local.yml')
    _res_config = update_nested_dict(source_config, local_source_config)
    etc_config = load_yml('/etc/dashcore/config.yml')
    res_config = update_nested_dict(_res_config, etc_config)
    config = Config(**res_config)

    return config


def get_db_connector(db_config=get_config().db):
    return RedisConnector(db_config)
