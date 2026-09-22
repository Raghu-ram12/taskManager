from taskmanager.queries import QueryManager
from taskmanager.models import User,UserCreate,TaskCreate
from fastapi import FastAPI 
import uvicorn 

manger=QueryManager() 

app=FastAPI() 

@app.post("/user/register")
def register_user(newUser:UserCreate):

    user_id=manger.createNewUser(newUser) 

    return{
        "user_id":user_id
    }

@app.post("/user/addtask")
def addTask(newtask:TaskCreate,user_id:int):

    task_id=manger.createTask(user_id,newtask)
    
    return {
        "user_id":user_id,
        "task_id":task_id,

    }
@app.delete("/user/task/{user_id}")
def delete_task(user_id:int,task_id:int):

    manger.deleteTask(user_id,task_id)

    return True 
@app.patch("/user/update/{user_id}/{parameter}")
def update_user(user_id: int, parameter: str, new_value: str):
    return manger.updateUser(user_id, parameter, new_value)

if __name__=="__main__":
    
    import uvicorn 

    uvicorn.run("main:app",reload=True) 

