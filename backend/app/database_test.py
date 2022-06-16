from ctypes import util
from uuid import uuid4
from database import Database
import repository
import psycopg2
import pytest
import utils
import exception
import os

user = repository.UserRepository()
task = repository.TaskRepository()


def test_database_connect():
    db = Database()
    db.connect()
    cur = db.execute("SELECT version()")
    db_version = cur.fetchone()


def test_add_user():
    new_user = utils.create_random_user()
    user.add(new_user)
    user_obj = user.get(id=new_user.id)
    assert user_obj.first_name == new_user.first_name
    assert user_obj.last_name == new_user.last_name
    assert user_obj.id == new_user.id


def test_update_user():
    updated_user = utils.create_random_user()
    user.add(updated_user)
    updated_user.update_password("mynewpassyay!")
    user.update(updated_user)
    user_obj = user.get(id=updated_user.id)
    assert user_obj.first_name == updated_user.first_name
    assert user_obj.last_name == updated_user.last_name
    assert user_obj.authenticate("mynewpassyay!")
    assert user_obj.id == updated_user.id


def test_delete_user():
    user_to_be_deleted = utils.create_random_user()
    user.add(user_to_be_deleted)
    user.delete(user_to_be_deleted.id)
    with pytest.raises(exception.UserNotFound):
        user.get(id=user_to_be_deleted.id)


def test_add_task():
    new_user = utils.create_random_user()
    user.add(new_user)
    new_task = utils.create_random_task(owner_id=new_user.id)
    task.add(new_task)
    task_objects = task.get(id=new_task.owner_id)
    if new_task not in task_objects:
        assert False


def test_update_task():
    new_user = utils.create_random_user()
    user.add(new_user)
    new_task = utils.create_random_task(owner_id=new_user.id)
    task.add(new_task)
    new_task.description = "I am new description"
    task.update(new_task)
    task_objects = task.get(id=new_task.owner_id)
    if new_task not in task_objects:
        assert False


def test_delete_task():
    new_user = utils.create_random_user()
    user.add(new_user)
    new_task = utils.create_random_task(owner_id=new_user.id)
    task.add(new_task)
    task.delete(id=new_task.id)
    task_objects = task.get(id=new_task.owner_id)
    if new_task in task_objects:
        assert False
