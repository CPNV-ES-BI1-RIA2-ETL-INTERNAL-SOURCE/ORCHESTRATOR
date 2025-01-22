from pydantic import BaseModel
from typing import List


class URLParams(BaseModel):
    country: str
    resource: str
    stop: str

class QueryParams(BaseModel):
    date: str

class DataItem(BaseModel):
    country: str
    resource: str
    stop: str

class Params(BaseModel):
    url: URLParams
    query: QueryParams
    data: List[DataItem]

class Process(BaseModel):
    name: str
    params: Params

class RequestModel(BaseModel):
    processes: List[Process]





