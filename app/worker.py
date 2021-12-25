from os import environ
import time

from celery import Celery


celery_conf = {
    "broker": environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),
    "backend": environ.get("CELERY_RESULT_BACKEND", "rpc://guest:guest@localhost:5672"),
}
celery = Celery(
    celery_conf=__name__,
    broker=celery_conf.get("broker"),
    backend=celery_conf.get("backend"),
)


@celery.task(name="delay_task")
def delay_task(delay):
    time.sleep(delay)
    return True
