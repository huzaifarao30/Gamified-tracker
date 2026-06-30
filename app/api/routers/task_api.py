from typing import List
from bson import ObjectId, errors as bson_errors  # ADDED: Added bson_errors to catch bad ID formats
from fastapi import APIRouter, HTTPException, status
from pymongo.errors import PyMongoError

from app.core.database import task_collection
from app.schemas.task_schemas import taskCreate, taskResponse, taskUpdate

taskRouter = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_object_id(id_str: str):
    try:
        return ObjectId(id_str)
    except bson_errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid ID format"
        )

@taskRouter.post("/", response_model=taskResponse, status_code=status.HTTP_201_CREATED)
def create_task(taskdata: taskCreate):
    try:
        task_dict = taskdata.model_dump()
        result = task_collection.insert_one(task_dict)
        task_dict["id"] = str(result.inserted_id)
        return task_dict
    except PyMongoError as e:
        print(f"Database insertion failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the task.",
        ) from e

@taskRouter.get("/", response_model=List[taskResponse])
def get_all_tasks():
    try:
        tasks = list(task_collection.find({}))
        for task in tasks:
            task["id"] = str(task.pop("_id"))
        return tasks
    except PyMongoError as e:
        print(f"Database fetch failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while fetching tasks.",
        ) from e

@taskRouter.get("/{task_id}", response_model=taskResponse)
def get_task(task_id: str):
    obj_id = get_object_id(task_id)
    try:
        task = task_collection.find_one({"_id": obj_id})
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="Database error") from e

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

    task["id"] = str(task.pop("_id"))
    return task

@taskRouter.patch("/{task_id}", response_model=taskResponse)
def update_task(task_id: str, update_data: taskUpdate):
    obj_id = get_object_id(task_id)
    try:
        update_dict = update_data.model_dump(exclude_unset=True)
        result = task_collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": update_dict},
            return_document=True,
        )
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="Database error") from e

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

    result["id"] = str(result.pop("_id"))
    return result

@taskRouter.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: str):
    obj_id = get_object_id(task_id)
    try:
        result = task_collection.delete_one({"_id": obj_id})
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="Database error") from e

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

    return {"message": f"Task {task_id} deleted successfully"}