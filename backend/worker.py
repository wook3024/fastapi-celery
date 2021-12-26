import time

from . import celery, ray
from .utils.save import save_image_data


@celery.task(name="save image")
def save_image_task(contents: str, save_image_path: str, delay: int = 0) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return "save path: {}, image shape: {}, delay: {}s".format(
        save_image_path, image_shape, delay
    )


def default_multiprocessing_task(
    contents: str, save_image_path: str, delay: int = 0
) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return "save path: {}, image shape: {}, delay: {}s".format(
        save_image_path, image_shape, delay
    )


@celery.task
def celery_multiprocessing_task(
    contents: str, save_image_path: str, delay: int = 0
) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return "save path: {}, image shape: {}, delay: {}s".format(
        save_image_path, image_shape, delay
    )


@ray.remote
def ray_multiprocessing_task(
    contents: str, save_image_path: str, delay: int = 0
) -> str:
    image_shape = save_image_data(contents, save_image_path)
    time.sleep(delay)
    return "save path: {}, image shape: {}, delay: {}s".format(
        save_image_path, image_shape, delay
    )
