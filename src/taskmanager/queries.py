
from taskmanager.schemas import get_connection,init_db

class QueryManager():

    def __init__(self):

        init_db() 
        self.conn=get_connection() 
    
    def createNewUser(self):
        pass 
    def updateUser(self):
        pass 
    def deleteUser(self):
        pass 
    def createTask(self):
        pass 
    def deleteTask(self):
        pass 
    def updateTask(self):
        pass 
    def completeTask(self):
        pass 
    def getTaskStatus(self):
        pass 
    

