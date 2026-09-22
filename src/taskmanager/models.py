from pydantic import BaseModel,EmailStr 
from typing import Optional


class UserCreate(BaseModel):
    
    first_name : str
    second_name:str
    email : EmailStr 
    password:str  
class TaskCreate(BaseModel):

    task_name:str 
    task_status:int 
    priority:int 
    deadline:str

class User(BaseModel):

    first_name : str
    second_name:str
    user_id:int
    email : EmailStr 
    password:str  
    


class Task(BaseModel):

    task_id :Optional[int]=None
    task_name:str 
    task_status:int 
    priority:int 
    CREATED_DATE:str 
    DEADLINE:str 

