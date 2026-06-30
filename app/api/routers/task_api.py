from fastapi import APIRouter , HTTPException ,status
from typing import List
from app.schemas.task_schemas import taskCreate , taskResponse , taskUpdate
from app.core.fake_db import task_db,tasks_counter

taskRouter = APIRouter(prefix="/tasks" , tags = ["Tasks"])

@taskRouter.post("/" , response_model=taskResponse , status_code=status.HTTP_201_CREATED)
def create_task(taskdata : taskCreate):
    global tasks_counter
    new_task = {"id" : tasks_counter, "name" : taskdata.name , "difficulty" : taskdata.difficulty , "completed" : False}
    task_db[tasks_counter] = new_task
    tasks_counter += 1
    return new_task

@taskRouter.get("/tasks", response_model=List[taskResponse])
def get_all_tasks():
    return list(task_db.values())

@taskRouter.get("/tasks/{task_id}", response_model=taskResponse)
def get_task(task_id: int):
    if task_id not in task_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task with ID {task_id} not found."
        )
    
    return task_db[task_id]

@taskRouter.patch("/tasks/{task_id}", response_model=taskResponse)
def update_task(task_id: int, update_data: taskUpdate):
    if task_id not in task_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found."
        )
    existing_task = task_db[task_id]
    update_dictionary = update_data.model_dump(exclude_unset=True)
    for key, value in update_dictionary.items():
        existing_task[key] = value
    return existing_task

@taskRouter.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    if task_id not in task_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found."
        )
    
    del task_db[task_id]
    
    return {"message": f"Task {task_id} deleted successfully"}



