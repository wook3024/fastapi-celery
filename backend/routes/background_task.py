import time
import time
import base64

from os import environ
from httpx import Client
from typing import List
from fastapi import UploadFile, File, APIRouter
from pathlib import Path, PurePath
from datetime import datetime
from celery.result import AsyncResult
from alive_progress import alive_bar
from multiprocessing import Process
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse, PlainTextResponse

from .. import schemas
from ..worker import (
    save_image_task,
    default_multiprocessing_task,
    ray_multiprocessing_task,
    celery_multiprocessing_task,
)

router = APIRouter()
save_image_dir_path = Path(
    environ.get("BASE_LOG_PATH", "/tmp"),
    environ.get("LOG_FOLDER_NAME", "logs"),
    environ.get("RECORD_DATE", datetime.now().strftime("%Y-%m-%d")),
    environ.get("IMAGE_FOLDER_NAME", "images"),
)


@router.post("", status_code=201)
async def run_task(delay: int = 1, file: UploadFile = File(...)) -> ORJSONResponse:
    contents = await file.read()
    encoded_contents = jsonable_encoder(base64.b64encode(contents))
    save_image_name = "{fn}.jpg".format(fn=PurePath(file.filename).stem)
    save_image_path = save_image_dir_path / save_image_name
    task = save_image_task.delay(encoded_contents, save_image_path.as_posix(), delay)
    return ORJSONResponse(content={"id": task.id})


@router.get("/{task_id}", status_code=200)
async def get_status(task_id: str) -> ORJSONResponse:
    task_result = AsyncResult(task_id)
    result = {"id": task_id, "status": task_result.state, "result": task_result.result}
    return ORJSONResponse(content=result)


@router.post("/multiprocessing/comparison", status_code=201)
async def run_multiple_task(
    task_info: schemas.MultipleTask,
    file: UploadFile = File(...),
) -> ORJSONResponse:
    """
    **default |████████████████████████████████████████| 10/10 [100%] in 31.2s (0.32/s)**\n
    **ray |████████████████████████████████████████| 10/10 [100%] in 0.7s (13.84/s)**\n
    **celery |████████████████████████████████████████| 10/10 [100%] in 18.8s (0.53/s)**
    """
    result = {}
    for method in task_info.method_list:
        with alive_bar(task_info.count, title=method) as bar:
            start_time = time.time()
            for _ in range(task_info.count):
                if method == "default":
                    p = Process(
                        target=default_multiprocessing_task,
                        args=(file, task_info.delay),
                    )
                    p.start()
                if method == "ray":
                    ray_multiprocessing_task.remote(file, task_info.delay)
                if method == "celery":
                    celery_multiprocessing_task.delay(file, task_info.delay)
                bar()
            end_time = time.time()
            result[method] = "{}s".format(round(end_time - start_time, 3))
    return ORJSONResponse(content=result)


@router.post("/request/multiple", status_code=200)
async def run_multiple_requests(
    request_info: schemas.MultipleRequest,
    files: List[UploadFile] = File(...),
) -> PlainTextResponse:
    client = Client()
    with alive_bar(len(files)) as bar:
        for file in files:
            response = client.post(
                url="http://{address}:{port}/{endpoint}".format(
                    address=request_info.address,
                    port=request_info.port,
                    endpoint=request_info.endpoint,
                ),
                json={"delay": request_info.delay, "file": file},
                timeout=request_info.timeout,
                headers={"Content-Type": "application/json"},
            )
            result = response.json()
            assert "id" in result
            bar()
    client.close()
    return PlainTextResponse(content="\n")
