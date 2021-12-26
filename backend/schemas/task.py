from typing import List
from pydantic import BaseModel


class MultipleTask(BaseModel):
    count: int = 10
    delay: int = 1
    method_list: List = ["ray", "default", "celery"]


class MultipleRequest(BaseModel):
    address: str = "localhost"
    port: int = 8000
    endpoint: str = "tasks"
    delay: str = "1"
    timeout: int = 300
