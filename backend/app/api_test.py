import pytest
import requests
import utils
from repository import UserRepository, TaskRepository
from model import Task, User
from datetime import datetime

host = "http://127.0.0.1:5000/"


def test_register_user():
    first_name = utils.generate_random_string(5)
    last_name = utils.generate_random_string(5)
    email = "{}@hotmail.com".format(utils.generate_random_string(10))
    password = utils.generate_random_string(8)
    data = {
        "user": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }
    }
    resp = requests.post(host + "register_user", json=data)
    print(resp.json())
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=email)
    print(user)
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.authenticate(password)


def test_login_user():
    user = utils.create_random_user()
    data = {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
    }
    resp = requests.post(host + "register_user", json=data)
    resp = requests.get(host + "login", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    assert user.id == resp.json()["user"]["id"]


def test_create_task():
    user = utils.create_random_user()
    data = {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
    }
    resp = requests.post(host + "register_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    task = utils.create_random_task(owner_id=user.id)
    desc = utils.generate_random_string(15)
    data = {"task": {"owner_id": user.id, "description": desc}}

    resp = requests.post(host + "create_task", json=data)
    task_repo = TaskRepository()
    task = task_repo.get(id=user.id)[0]
    assert task.owner_id == user.id
    assert task.description == desc


def test_get_task():
    user = utils.create_random_user()
    data = {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
    }
    resp = requests.post(host + "register_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    task = utils.create_random_task(owner_id=user.id)
    descriptions = []
    num_of_tasks = 10
    for x in range(num_of_tasks):
        desc = utils.generate_random_string(15)
        descriptions.append(desc)
        data = {"task": {"owner_id": user.id, "description": desc}}
        resp = requests.post(host + "create_task", json=data)

    task_repo = TaskRepository()
    tasks = task_repo.get(user.id)
    assert len(tasks) == num_of_tasks
    for x in range(num_of_tasks):
        assert descriptions[x] in list(map(lambda x: x.description, tasks))


def test_edit_task():
    user = utils.create_random_user()
    data = {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
    }
    resp = requests.post(host + "register_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    data = {
        "task": {"owner_id": user.id, "description": utils.generate_random_string(15)}
    }
    resp = requests.post(host + "create_task", json=data)
    task_repo = TaskRepository()
    task = task_repo.get(user.id)[0]
    edited_task = {
        "task": {
            "id": task.id,
            "due_time": "2025-05-25",
            "done": "true",
            "description": "edited task I am",
        }
    }
    resp = requests.post(host + "edit_task", json=edited_task)
    edit_task = task_repo.get(user.id)[0]
    assert task.id == edit_task.id
    assert datetime(2025, 5, 25) == edit_task.due_time
    assert edit_task.done
    assert "edited task I am" == edit_task.description


def test_delete_task():
    user = utils.create_random_user()
    data = {
        "user": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
        }
    }
    resp = requests.post(host + "register_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    data = {
        "task": {"owner_id": user.id, "description": utils.generate_random_string(15)}
    }
    resp = requests.post(host + "create_task", json=data)
    task_repo = TaskRepository()
    task = task_repo.get(user.id)[0]
    assert task_repo.get_by_id(task.id)
    task_repo.delete(task.id)
    assert not task_repo.get_by_id(task.id)