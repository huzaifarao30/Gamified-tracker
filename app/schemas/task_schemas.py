from pydantic import BaseModel,Field
from enum import Enum

class DifficultyEnum(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class taskCreate(BaseModel):
    name : str = Field(..., min_length=1)
    difficulty : DifficultyEnum
    completed : bool = False 

class taskResponse(taskCreate):
    id : str

class taskUpdate(BaseModel):
    name : str | None = Field(None , min_length=1)
    difficulty : DifficultyEnum | None = Field(None , min_length=3)
    completed : bool | None = None



    