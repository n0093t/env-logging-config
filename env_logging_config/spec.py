import json
from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel, BaseSettings, Field, validator


def json_decoder(loads: Callable = json.loads) -> Any:
    def decoder(value: str):
        if not isinstance(value, str):
            return value

        return loads(value)

    return decoder


class Handler(BaseModel):
    klass: str = Field(alias='class')
    level: Optional[str]
    formatter: Optional[str]
    filters: Optional[List[str]]

    _json_decoder = validator(
        'filters',
        pre=True,
        allow_reuse=True
    )(json_decoder())


class Handlers(BaseModel):
    __root__: Dict[str, Handler]


class Formatter(BaseModel):
    klass: Optional[str] = Field(alias='()')
    format: Optional[str]
    datefmt: Optional[str]
    style: Optional[str]
    validate_: Optional[bool] = Field(alias='validate')

    class Config:
        allow_population_by_field_name: bool = True


class Formatters(BaseModel):
    __root__: Dict[str, Formatter]


class Logger(BaseModel):
    level: Optional[str]
    propagate: Optional[bool]
    filters: Optional[List[str]]
    handlers: Optional[List[str]]

    _json_decoder = validator(
        'filters',
        'handlers',
        pre=True,
        allow_reuse=True
    )(json_decoder())


class Loggers(BaseModel):
    __root__: Dict[str, Logger]


class Filter(BaseModel):
    name: str


class Filters(BaseModel):
    __root__: Dict[str, Filter]


class LoggingSettings(BaseSettings):
    version: Literal['1'] = '1'
    disable_existing_loggers: Optional[bool]
    incremental: Optional[bool]
    root: Optional[Logger]
    formatters: Optional[Formatters]
    handlers: Optional[Handlers]
    loggers: Optional[Loggers]
    filters: Optional[Filters]
