import ray
import psutil

from os import environ
from celery import Celery


num_logical_cpus = psutil.cpu_count(logical=False)
ray.init(num_cpus=num_logical_cpus)

celery_conf = {
    "broker": environ.get(
        "CELERY_BROKER_URL",
        "redis://localhost:6379",
    ),
    "backend": environ.get(
        "CELERY_RESULT_BACKEND",
        "rpc://guest:guest@localhost:5672",
    ),
}
celery = Celery(
    celery_conf=__name__,
    broker=celery_conf.get("broker"),
    backend=celery_conf.get("backend"),
)

__all__ = [
    "ray",
    "celery",
]
