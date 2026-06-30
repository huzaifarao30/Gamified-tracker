from fastapi import FastAPI
from app.api.routers.task_api import taskRouter

app = FastAPI(title="Task Game API")
app.include_router(taskRouter)
