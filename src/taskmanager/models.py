from pydantic import BaseModel,EmailStr 
from datetime import date
from typing import Optional 

class User(BaseModel):

    user_id:Optional[int] =None
    first_name : str
    second_name:str
    email : EmailStr 

class Task(BaseModel):

    task_id: Optional[int] = None 
    user_id: int
    task_name: str 
    task_status: str = "NOT STARTED"
    priority: int 
    difficulty: str 
    created_date: Optional[str] = None
    deadline: str

Task.model_rebuild()
