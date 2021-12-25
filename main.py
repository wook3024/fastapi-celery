from fastapi import Body, FastAPI
from celery.result import AsyncResult
from fastapi.responses import ORJSONResponse

from app.worker import delay_task


app = FastAPI(default_response_class=ORJSONResponse)


@app.post("/tasks", status_code=201)
def run_task(delay: int = Body(...)) -> ORJSONResponse:
    task = delay_task.delay(delay)
    return ORJSONResponse(content={"id": task.id})


@app.get("/tasks/{task_id}", status_code=200)
def get_status(task_id: str) -> ORJSONResponse:
    task_result = AsyncResult(task_id)
    result = {"id": task_id, "status": task_result.state, "result": task_result.result}
    return ORJSONResponse(content=result)
