import pytest
import requests
import utils
from repository import UserRepository, TaskRepository
from model import Task, User
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("ADDRESS")


def test_register_user():
    first_name = utils.generate_random_string(5)
    last_name = utils.generate_random_string(5)
    email = "{}@hotmail.com".format(utils.generate_random_string(10))
    password = utils.generate_random_string(8)
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
    }
    resp = requests.post(host + "register_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=email)
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.authenticate(password)


def test_login_user():
    user = utils.create_random_user()
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
    }
    resp = requests.post(host + "register_user", json=data)
    resp = requests.post(host + "login_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    assert utils.jwt_decode(resp.json()["token"]) == user.id


def test_create_task():
    user = utils.create_random_user()
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
    }
    resp = requests.post(host + "register_user", json=data)
    resp = requests.post(host + "login_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    task = utils.create_random_task(owner_id=user.id)
    desc = utils.generate_random_string(15)
    data = {"description": desc, "token": resp.json()["token"]}

    resp = requests.post(host + "create_task", json=data)
    task_repo = TaskRepository()
    task = task_repo.get(id=user.id)[0]
    assert task.owner_id == user.id
    assert task.description == desc


def test_get_task():
    user = utils.create_random_user()
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
    }
    resp = requests.post(host + "register_user", json=data)
    resp = requests.post(host + "login_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    task = utils.create_random_task(owner_id=user.id)
    descriptions = []
    num_of_tasks = 10
    for x in range(num_of_tasks):
        desc = utils.generate_random_string(15)
        descriptions.append(desc)
        data = {"description": desc, "token": resp.json()["token"]}
        resp_post = requests.post(host + "create_task", json=data)

    task_repo = TaskRepository()
    tasks = task_repo.get(user.id)
    assert len(tasks) == num_of_tasks
    for x in range(num_of_tasks):
        assert descriptions[x] in list(map(lambda x: x.description, tasks))


def test_edit_task():
    user = utils.create_random_user()
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
    }
    resp = requests.post(host + "register_user", json=data)
    resp = requests.post(host + "login_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    data = {
        "token": resp.json()["token"],
        "description": utils.generate_random_string(15),
    }
    resp_post = requests.post(host + "create_task", json=data)
    task_repo = TaskRepository()
    task = task_repo.get(user.id)[0]
    edited_task = {
        "due_time": "Thu, 14 Jul 2022 13:21:15 GMT",
        "done": "true",
        "description": "edited task I am",
        "id": task.id,
        "token": resp.json()["token"],
    }
    resp = requests.post(host + "edit_task", json=edited_task)
    edit_task = task_repo.get(user.id)[0]
    assert task.id == edit_task.id
    assert datetime(2022, 7, 14, 13, 21, 15) == edit_task.due_time
    assert edit_task.done
    assert "edited task I am" == edit_task.description


def test_delete_task():
    user = utils.create_random_user()
    data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
    }
    resp = requests.post(host + "register_user", json=data)
    resp = requests.post(host + "login_user", json=data)
    user_repo = UserRepository()
    user = user_repo.get(by="email", id=user.email)
    data = {
        "owner_id": str(user.id),
        "description": utils.generate_random_string(15),
        "token": resp.json()["token"],
    }
    resp = requests.post(host + "create_task", json=data)
    task_repo = TaskRepository()
    task = task_repo.get(user.id)[0]
    assert task_repo.get_by_id(task.id)
    resp = requests.post(host + "delete_task", json={"id": str(task.id)})
    assert not task_repo.get_by_id(task.id)
