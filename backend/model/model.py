from dataclasses import dataclass, field
import hashlib
from re import A
import uuid
import datetime
import random
import string
import copy
from collections import defaultdict
from itertools import groupby

# dataclass documentation https://docs.python.org/3/library/dataclasses.html


def generate_hexdigest(string: str) -> str:  # Assuming string to be in utf-8 format.
    return hashlib.sha256(bytes(string, " utf-8 ")).hexdigest()


@dataclass
class Task:
    """A class containing data for tasks. Using dataclass because they are used for classes that primarily store data"""

    id: uuid
    creation_time: datetime
    owner_id: int
    description: str = ""
    done: bool = False


@dataclass
class User:
    """A class containing data for registered User in the system"""

    id: uuid
    first_name: str
    last_name: str
    password_hash: str

    def authenticate(self, password: str) -> bool:
        return generate_hexdigest(password) == self.password_hash


@dataclass
class App:
    """API Interface of application with which backend communicates with the database and sends query results to frontend after requests"""

    # Data Stuctures for holding user and task data
    user_ids_to_todolist: defaultdict(list) = field(
        default_factory=lambda: defaultdict(list)
    )

    # A key-value pair data structure in which keys are user-ids and values are to-do lists corresponding to those user-ids
    users = []

    # Methods

    def register_user(
        self, id: uuid, first_name: str, last_name: str, password_hash: str
    ):
        self.users.append(User(id, first_name, last_name, password_hash))

    def check_user(self, authenticate_user_id: uuid):
        for user in self.users:
            if user.id == authenticate_user_id:
                return True
        return False

    def get_tasks_by_day(self, owner_id: uuid):
        tasks = self.user_ids_to_todolist[owner_id]
        ordered_by_day = [
            list(v) for i, v in groupby(tasks, lambda x: x.creation_time.day)
        ]
        print("\nPrinting Tasks in order for User {}\n".format(owner_id))
        for day in ordered_by_day:
            print(day)
            print("")

    def add_task(self, task: Task) -> None:
        if self.check_user(task.owner_id):
            print("PRESENT")
            self.user_ids_to_todolist[task.owner_id].append(copy.deepcopy(task))

    def print_tasks(self) -> None:  # Remove Eventually
        print(
            "\nPrinting Tasks for Total {} Users \n".format(
                len(self.user_ids_to_todolist)
            )
        )
        for k, value in self.user_ids_to_todolist.items():
            print(k)
            for task in value:
                print(task)
            print("")

    def change_order(self, new_task: Task, indx: int) -> None:
        tasks = self.user_ids_to_todolist[new_task.owner_id]
        task = tasks[tasks.index(new_task)]
        tasks.remove(task)
        tasks.insert(indx, task)

    def delete_task(self, delete_task: Task) -> None:
        tasks = self.user_ids_to_todolist[delete_task.owner_id]
        tasks.remove(delete_task)

    def edit_task(self, edited_task: Task) -> None:
        tasks = self.user_ids_to_todolist[edited_task.owner_id]
        indx = list(map(lambda x: x.id, tasks)).index(edited_task.id)
        tasks[indx] = edited_task

    def mark(self, change_task: Task, mark: bool = True) -> None:
        tasks = self.user_ids_to_todolist[change_task.owner_id]
        indx = list(map(lambda x: x.id, tasks)).index(change_task.id)
        tasks[indx].done = mark
