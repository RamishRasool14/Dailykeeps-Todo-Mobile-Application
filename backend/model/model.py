from dataclasses import dataclass
import hashlib
from re import A
import uuid
import datetime
import random
import string
import copy

# Datatclass documentation https://docs.python.org/3/library/dataclasses.html

def generate_hexdigest(string : str) -> str:  # Assuming string to be in utf-8 format.
    return hashlib.sha256( bytes(string, ' utf-8 ') ).hexdigest()

@dataclass(init=True, repr=True, order=True, frozen=False)
class Task:
    """ A class containing data for tasks. Using dataclass because they are used for classes that primarily store data """
    id: int
    # order_id: int
    creation_time: datetime
    owner_id: int
    title: str = ""
    description: str = ""
    done: bool = False

@dataclass(init=True, repr=True, order=True, frozen=True)
class User:
    """ A class containing data for registered User in the system """
    id: uuid
    first_name: str
    last_name: str
    password_hash: str

    def authenticate(self, password : str) -> bool:
        return True if generate_hexdigest(password) == self.password_hash else False

class App:
    """ API Interface of application with which backend communicates with the database and sends query results to frontend after requests """
    tasks: list = []
    users: list = []

    def __del__(self):
        self.tasks = []
        self.users = []

    def addTask(self,task):
        # order_id = len(self.tasks) 
        self.tasks.append(copy.deepcopy(task))

    def createRandomTask(self):
        length = 10
        return Task(uuid.uuid4(), datetime.datetime.now(), random.randint(0,1000), ''.join(random.choices(string.ascii_lowercase + string.digits, k = length)), ''.join(random.choices(string.ascii_lowercase + string.digits, k = length*2)) )

    def printTasks(self):
        print("\nPrinting Total {} Task \n".format(len(self.tasks)) )
        for task in self.tasks:
            print(task)
            print("")
    
    def changeOrder(self, task1, task2):
        ind1 = self.tasks.index(task1)
        ind2 = self.tasks.index(task2)
        self.tasks.remove(task1)
        self.tasks.remove(task2)

        if ind1 < ind2:
            self.tasks.insert(ind1,task2)
            self.tasks.insert(ind2,task1)
        else:
            self.tasks.insert(ind2,task1)
            self.tasks.insert(ind1,task2)

    def deleteTask(self, task):
        self.tasks.remove(task)

    def editTask(self, ind, editedTask):
        self.tasks.remove(self.tasks[ind])
        self.tasks.insert(ind,editedTask)

    def markComplete(self, ind):
        self.tasks[ind].done = True 
    