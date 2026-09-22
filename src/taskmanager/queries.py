import sqlite3
from taskmanager.models import User,Task,TaskCreate,UserCreate
from taskmanager.schemas import get_connection, init_db

class QueryManager:

    def __init__(self):
        
        init_db() 
        
    
    def createNewUser(self, newuser:UserCreate) -> Optional[int]:

        """Inserts a new user and returns their auto-incremented ID.""" 

        query = "INSERT INTO users (FIRST_NAME,SECOND_NAME,EMAIL,PASSWORD) VALUES (?,?,?,?)" 

        user_data = newuser.model_dump(exclude_none=True)

        params = (
        newuser.first_name,
        newuser.second_name,  
        newuser.email,
        newuser.password
            )

        try:
            with get_connection() as conn:
                cursor = conn.cursor() 
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid 

        except sqlite3.IntegrityError as e:
            print(f"Database Error: {e}") 
            return None 

        
    def updateUser(self, user_id: int, parameter: str, new_value: str) -> bool:
        """Updates a user's details. Returns True if successful."""
        
        
        allowed_parameters = {"first_name", "second_name", "email", "password"} 

        if parameter not in allowed_parameters:

            raise ValueError(f"Invalid update parameter: {parameter}")

    
        query = f"UPDATE users SET {parameter} = ? WHERE USER_ID = ?"

        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(query, (new_value, user_id))
            conn.commit()
            return cursor.rowcount > 0


    def deleteUser(self, user_id: int) -> bool:

        """Deletes a user by ID. Returns True if successful."""
        query = "DELETE FROM users WHERE id = ?" 


        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    

    def createTask(self, user_id: int,newTask : TaskCreate) -> int:

        """Creates a task linked to a user. Returns the new task ID."""

        query = "INSERT INTO tasks (USER_ID, TASK_NAME,PRIORITY,DEADLINE) VALUES (?, ?, ?, ?)" 

        data_dict=newTask.model_dump(exclude_none=True)  

        params=(
            user_id,
            data_dict.get("task_name"),
            data_dict.get("priority"),
            data_dict.get("deadline")

        )

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query,params)
            conn.commit()
            return cursor.lastrowid

    def deleteTask(self, user_id:int,task_id: int) -> bool:

        """Deletes a task by ID. Returns True if successful."""

        query = "DELETE FROM tasks WHERE USER_ID = ? and TASK_ID=?"

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,task_id))
            conn.commit()
            return cursor.rowcount > 0

    def updateTask(self, task_id,parameter:str,new_value:str) -> bool: 

        """Updates a task's parameters """ 

        query = f"UPDATE tasks SET {parameter}=? WHERE id =?" 

        if parameter not in {"task_name","deadline","priority","task_status"}:

            raise ValueError(f"Invalid update parameter {parameter}")

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (new_value,task_id))
            conn.commit()
            return cursor.rowcount > 0

    def completeTask(self, task_id: int) -> bool:

        """Marks a task as completed (sets completed to 1)."""

        query = "UPDATE tasks SET completed = 1 WHERE id = ?" 

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    def getTaskStatus(self, task_id: int) -> Optional[Dict[str, Any]]: 

        """Fetches a specific task's row data to check its status."""

        query = "select completed from tasks where task_id=?" 

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (task_id,))
            row = cursor.fetchone()
            
            if row is None:
                return None
                
    
            if isinstance(row, dict):
                row["completed"] = bool(row["completed"])
                return row
            
            return {
                "id": row[0],
                "title": row[1],
                "completed": bool(row[2])
            }

