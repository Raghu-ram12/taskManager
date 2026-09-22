
from taskmanager.schemas import get_connection,init_db
from taskmanager.models import User,Task
import logging


logging.basicConfig(
    filename='app.log', 
    filemode='w',            
    level=logging.DEBUG,     
    format='%(asctime)s - %(levelname)s - %(message)s') 


class QueryManager():

    def __init__(self): 

        self.conn=get_connection()
        init_db(connection=self.conn) 
    
    def createNewUser(self,newUser:User):

        data_dict = newUser.model_dump(exclude_none=True)  

        cursor = self.conn.cursor()
        columns = ", ".join(data_dict.keys())
        placeholders = ", ".join(["?"] * len(data_dict))

        query = f"INSERT INTO USERS ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data_dict.values()))
        self.conn.commit()

        logging.info(f"new user added with id {cursor.lastrowid}") 

        return cursor.lastrowid

       
    def updateUser(self,user_id:int,parameter:str,new_value:str): 

        query=f"UPDATE USERS SET {parameter} = {new_value} WHERE USER_ID={user_id}" 

        cursor=self.conn.cursor() 

        cursor.execute(query) 

        logging.info(f"update user with {user_id} parameter :{parameter} to {new_value}") 


    def deleteUser(self,user_id : int):

        cursor=self.conn.cursor() 

        query=f"DELETE FROM USERS WHERE USER_ID = ?" 

        cursor.execute(query,[user_id])  

        self.conn.commit()
        logging.warning("user with id {user_id} deleted from database") 

 

    def createTask(self,newTask:newTask): 

        cursor=self.conn.cursor() 

        data_dict=newTask.model_dump(exclude_none=True)

        placeholders = ", ".join(["?"] * len(data_dict)) 

        columns = ", ".join(data_dict.keys())   

        query=f"INSERT INTO TASKS ({columns}) VALUES ({placeholders})"

        cursor.execute(query, tuple(data_dict.values())) 

        self.conn.commit() 
        
        logging.info(f"new task is created with id {cursor.lastrowid}") 
        cursor.close() 

        return cursor.lastrowid 

    def deleteTask(self,task_id:int):

        cursor=self.conn.cursor() 

        query="DELETE FROM TASKS WHERE TASK_ID=?" 

        cursor.execute(query,[task_id]) 

        logging.warning(f"task with id {task_id} deleted successfully") 

        cursor.close()  

    def updateTask(self,task_id:int,parameters:list[str],new_parameters:list[str]):

        cursor=self.conn.cursor() 

        for param,new_param in zip(parameters,new_parameters):

            query="UPDATE TASKS SET ? = ?" 

            for new_parm in new_parameters:

                cursor.execute(query,tuple(param,new_parm)) 
        
        logging.info(f"task with id {task_id} updated ") 

        cursor.close() 
                

    def completeTask(self,task_id:int):

        cursor=self.conn.cursor()

        query="UPDATE TASKS SET TASK_STATUS = ? WHERE TASK_ID=?"  

        cursor.execute(query,tuple("COMPLETED",task_id)) 

        logging.info("task with id {task_id}")
        
        cursor.close() 
        
    def getTaskStatus(self,task_id:int):

        cursor=self.conn.cursor() 

        query="SELECT TASK_STATUS FROM TASKS WHERE TASK_ID=?" 

        cursor.execute(query,tuple(task_id)) 

        logging.info("")
          
        return cursor.fetchall()  


    def getIdByName(self,name:str,user_id:int):

        cursor=self.conn.cursor() 
        
        query="SELECT TASK_ID FROM TASKS WHERE TASK_NAME=? AND USER_ID=?" 

        cursor.execute(query,tuple(name,user_id)) 

        


