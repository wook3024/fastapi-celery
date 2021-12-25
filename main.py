from fastapi import Body, FastAPI
from celery.result import AsyncResult
from fastapi.responses import JSONResponse

from app.worker import delay_task


app = FastAPI()


@app.post("/tasks", status_code=201)
def run_task(delay: int = Body(...)) -> JSONResponse:
    task = delay_task.delay(delay)
    return JSONResponse(content={"id": task.id})


@app.get("/tasks/{task_id}", status_code=200)
def get_status(task_id: str) -> JSONResponse:
    task_result = AsyncResult(task_id)
    result = {
        "id": task_id,
        "status": task_result.state,
        "result": task_result.result,
    }
    return JSONResponse(content=result)
