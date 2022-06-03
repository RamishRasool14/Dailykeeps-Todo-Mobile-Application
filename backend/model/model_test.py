import pytest
from model import App, Task
import uuid
import datetime
import random
import string
import copy
from collections import defaultdict


def create_random_task(owner_id: int):
    length = 10
    return Task(
        uuid.uuid4(),
        datetime.datetime.now(),
        owner_id,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=length)),
    )


def test_add_task():  # Creates random 10 tasks and tests if they are correctly added to the system
    app = App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        app.add_task(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))
    assert test_dict == app.dictionary


def test_change_order():  # Creates random 10 tasks and change order of the first and last task
    app = App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        app.add_task(task)
        tasks.append(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    ind1 = 0
    ind2 = 4

    test_dict[0].remove(tasks[4])
    test_dict[0].insert(ind1, tasks[4])

    app.change_order(tasks[ind2], ind1)
    assert test_dict == app.dictionary


def test_delete_task():
    app = App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        app.add_task(task)
        tasks.append(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    app.delete_task(tasks[3])
    test_dict[0].remove(tasks[3])

    assert test_dict == app.dictionary


def test_edit_task():
    app = App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        app.add_task(task)
        tasks.append(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    tasks[3].description = "Please edit the task Bro"
    app.edit_task(tasks[3])
    test_dict[0][3].description = "Please edit the task Bro"

    assert test_dict == app.dictionary


def test_mark_complete():
app = App()
tasks = []
test_dict = defaultdict(list)
for x in range(10):
    if x < 5:
        task = create_random_task(0)
    else:
        task = create_random_task(1)
    app.add_task(task)
    tasks.append(task)
    test_dict[task.owner_id].append(copy.deepcopy(task))

    tasks[3].done = True
    app.mark(tasks[3])
    test_dict[0][3].done = True
    assert test_dict == app.dictionary

    app.mark(tasks[3], False)
    test_dict[0][3].done = False
    assert test_dict == app.dictionary

# app = App()
# tasks = []
# test_dict = defaultdict(list)
# for x in range(10):
#     if x < 5:
#         task = create_random_task(0)
#     else:
#         task = create_random_task(1)
#     app.add_task(task)
#     tasks.append(task)
#     test_dict[task.owner_id].append(copy.deepcopy(task))

# ind1 = 0
# ind2 = 4

# test_dict[0].remove(tasks[4])
# test_dict[0].insert(ind1, tasks[4])

# app.change_order(tasks[ind2], ind1)
# app.print_tasks()
