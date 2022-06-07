import pytest
import model
import uuid
import datetime
import random
import string
import copy
from collections import defaultdict


def create_random_task(owner_id: uuid):
    length = 10
    return model.Task(
        uuid.uuid4(),
        datetime.datetime.now(),
        owner_id,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=length)),
    )


def create_random_user():
    length = 6
    return model.User(
        uuid.uuid4(),
        "".join(random.choices(string.ascii_lowercase + string.digits, k=length)),
        "".join(random.choices(string.ascii_lowercase + string.digits, k=length)),
        model.generate_hexdigest(
            "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
        ),
    )


def test_add_user():
    app = model.App()
    users = [create_random_user() for x in range(10)]

    for user in users:
        app.register_user(user.id, user.first_name, user.last_name, user.password_hash)

    for user in users:
        assert app.check_user(user.id)


def test_add_task():  # Creates random 10 tasks and tests if they are correctly added to the system
    app = model.App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        user = create_random_user()
        app.register_user(
            task.owner_id, user.first_name, user.last_name, user.password_hash
        )
        app.add_task(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    assert test_dict == app.user_ids_to_todolist


def test_change_order():  # Creates random 10 tasks and change order of the first and last task
    app = model.App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        user = create_random_user()
        app.register_user(
            task.owner_id, user.first_name, user.last_name, user.password_hash
        )
        app.add_task(task)
        tasks.append(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    ind1 = 0
    ind2 = 4

    test_dict[0].remove(tasks[4])
    test_dict[0].insert(ind1, tasks[4])

    app.change_order(tasks[ind2], ind1)
    assert test_dict == app.user_ids_to_todolist


def test_delete_task():
    app = model.App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        user = create_random_user()
        app.register_user(
            task.owner_id, user.first_name, user.last_name, user.password_hash
        )
        app.add_task(task)
        tasks.append(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    app.delete_task(tasks[3])
    test_dict[0].remove(tasks[3])

    assert test_dict == app.user_ids_to_todolist


def test_edit_task():
    app = model.App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        user = create_random_user()
        app.register_user(
            task.owner_id, user.first_name, user.last_name, user.password_hash
        )
        app.add_task(task)
        tasks.append(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    tasks[3].description = "Please edit the task Bro"
    app.edit_task(tasks[3])
    test_dict[0][3].description = "Please edit the task Bro"

    assert test_dict == app.user_ids_to_todolist


def test_mark_complete():
    app = model.App()
    tasks = []
    test_dict = defaultdict(list)
    for x in range(10):
        if x < 5:
            task = create_random_task(0)
        else:
            task = create_random_task(1)
        user = create_random_user()
        app.register_user(
            task.owner_id, user.first_name, user.last_name, user.password_hash
        )
        app.add_task(task)
        tasks.append(task)
        test_dict[task.owner_id].append(copy.deepcopy(task))

    tasks[3].done = True
    app.mark(tasks[3])
    test_dict[0][3].done = True
    assert test_dict == app.user_ids_to_todolist

    app.mark(tasks[3], False)
    test_dict[0][3].done = False
    assert test_dict == app.user_ids_to_todolist


def test_get_tasks_by_day():  # Creates a user with owner_id 1 and adds 2 tasks dated 2020/5/17, 3 tasks dated 2020/5/10 and 1 task dated 2020/5/16. Checks the method of get_tasks_by_day to see if it prints tasks correctly which it does
    app = model.App()
    tasks = []
    test_dict = defaultdict(list)

    task = model.Task(
        uuid.uuid4(),
        datetime.datetime(2020, 5, 17),
        1,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
    )
    user = create_random_user()
    user.id = task.owner_id
    app.register_user(user.id, user.first_name, user.last_name, user.password_hash)
    tasks.append(task)
    app.add_task(task)
    test_dict[task.owner_id].append(copy.deepcopy(task))

    task = model.Task(
        uuid.uuid4(),
        datetime.datetime(2020, 5, 17),
        1,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
    )
    tasks.append(task)
    app.add_task(task)
    test_dict[task.owner_id].append(copy.deepcopy(task))

    task = model.Task(
        uuid.uuid4(),
        datetime.datetime(2020, 5, 16),
        1,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
    )
    tasks.append(task)
    app.add_task(task)
    test_dict[task.owner_id].append(copy.deepcopy(task))

    task = model.Task(
        uuid.uuid4(),
        datetime.datetime(2020, 5, 10),
        1,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
    )
    tasks.append(task)
    app.add_task(task)
    test_dict[task.owner_id].append(copy.deepcopy(task))

    task = model.Task(
        uuid.uuid4(),
        datetime.datetime(2020, 5, 10),
        1,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
    )
    tasks.append(task)
    app.add_task(task)
    test_dict[task.owner_id].append(copy.deepcopy(task))
    task = model.Task(
        uuid.uuid4(),
        datetime.datetime(2020, 5, 10),
        1,
        "".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
    )
    tasks.append(task)
    app.add_task(task)
    test_dict[task.owner_id].append(copy.deepcopy(task))

    app.get_tasks_by_day(1)
