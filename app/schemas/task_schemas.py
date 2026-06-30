from pydantic import BaseModel,Field


class taskCreate(BaseModel):
    name : str = Field(..., min_length=1)
    difficulty : str = Field(... , min_length=3)
    completed : bool = False 

class taskResponse(taskCreate):
    id : int

class taskUpdate(BaseModel):
    name : str | None = Field(None , min_length=1)
    difficulty : str | None = Field(None , min_length=3)
    completed : bool | None = None



    