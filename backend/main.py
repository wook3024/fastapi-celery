from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .routes import background_task


app = FastAPI(
    title="Tasks queue with FastAPI and Celery",
    default_response_class=ORJSONResponse,
)
app.include_router(
    router=background_task.router,
    prefix="/background_task",
    tags=["Background task"],
)
