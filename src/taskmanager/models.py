from pydantic import BaseModel,EmailStr 

class User(BaseModel):
    
    first_name : str
    second_name:str
    user_id:int 
    email : EmailStr 

class Task(BaseModel):

    task_id :int 
    task_name:str 
    task_
