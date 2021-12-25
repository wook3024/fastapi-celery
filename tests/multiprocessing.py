import ray
import psutil
import numpy as np
from os import environ
from typing import Dict
from celery import Celery
from alive_progress import alive_bar


"""
    pure |████████████████████████████████████████| 10/10 [100%] in 0.0s (529.67/s)
    ray |████████████████████████████████████████| 10/10 [100%] in 0.6s (16.63/s)
    celery |████████████████████████████████████████| 10/10 [100%] in 25.4s (0.39/s)
"""


celery_conf = {
    "broker": environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),
    "backend": environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379"),
}
celery = Celery(
    celery_conf=__name__,
    broker=celery_conf.get("broker"),
    backend=celery_conf.get("backend"),
)

num_logical_cpus = psutil.cpu_count(logical=False)
ray.init(num_cpus=num_logical_cpus)


def pure_test(image: np.array) -> Dict:
    assert len(image.shape) == 3
    return {"status": True}


@ray.remote
def ray_test(image: np.array) -> Dict:
    assert len(image.shape) == 3
    return {"status": True}


@celery.task(serializer="pickle")
def celery_test(image: np.array) -> Dict:
    assert len(image.shape) == 3
    return {"status": True}


if __name__ == "__main__":
    count = 10
    rand_image = np.random.rand(3000, 3000, 3)
    for method in ["pure", "ray", "celery"]:
        with alive_bar(count, title=method) as bar:
            for i in range(count):
                if method == "pure":
                    pure_test(rand_image)
                if method == "ray":
                    ray_test.remote(rand_image)
                if method == "celery":
                    celery_test.apply_async(args=[rand_image])
                bar()
