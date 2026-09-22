from src.taskmanager.queries import QueryManager 

from src.taskmanager.models import User,Task


newUser=User(first_name="raghuram",second_name="pentela",email="raghurampentela@gmail.com")

manager=QueryManager() 

cursor=manager.conn.cursor() 


new_user_id=manager.createNewUser(newUser)

newtask=Task(user_id=new_user_id,task_name="exam",task_status="incomplete",priority=3,difficulty="LOW",created_date=None,deadline="2026-09-12")


manager.createTask(newtask) 

cursor.execute("SELECT * FROM USERS")  

userrows = cursor.fetchall()  

cursor.execute("SELECT * FROM TASKS")

taskrows=cursor.fetchall() 

for row in taskrows:

    print(row)


for row in userrows:
    print(row) 

