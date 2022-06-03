from dataclasses import dataclass
import enum
import hashlib
from re import A
import uuid
import datetime
import random
import string
import copy
from collections import defaultdict

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


class App:
    """API Interface of application with which backend communicates with the database and sends query results to frontend after requests"""

    dictionary = defaultdict(
        list
    )  # A key-value pair data structure in which keys are user-ids and values are to-do lists corresponding to those user-ids

    def add_task(self, task: Task) -> None:
        self.dictionary[task.owner_id].append(copy.deepcopy(task))

    def print_tasks(self) -> None:  # Remove Eventually
        print("\nPrinting Tasks for Total {} Users \n".format(len(self.dictionary)))
        for k, value in self.dictionary.items():
            print(k)
            # value = sorted(
            #     value, key=lambda x: x.creation_time
            # )  # Sorts date such that the most recently created task is printed first
            for task in value:
                print(task)
            print("")

    def change_order(self, new_task: Task, indx: int) -> None:
        tasks = self.dictionary[new_task.owner_id]
        tasks.remove(new_task)
        tasks.insert(indx, new_task)
        self.dictionary[new_task.owner_id] = tasks

    def delete_task(self, delete_task: Task) -> None:
        tasks = self.dictionary[delete_task.owner_id]
        tasks.remove(delete_task)
        self.dictionary[delete_task.owner_id] = tasks

    def edit_task(self, editedTask: Task) -> None:
        tasks = self.dictionary[editedTask.owner_id]
        for indx, task in enumerate(tasks):
            if editedTask.id == task.id:
                break
        tasks.remove(tasks[indx])
        tasks.insert(indx, editedTask)
        self.dictionary[editedTask.owner_id] = tasks

    def mark(self, change_task: Task, mark: bool = True) -> None:
        tasks = self.dictionary[change_task.owner_id]
        for indx, task in enumerate(tasks):
            if change_task.id == task.id:
                break
        if mark:
            tasks[indx].done = True
        else:
            tasks[indx].done = False
