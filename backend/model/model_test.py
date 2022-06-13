import pytest
import model
import uuid
import datetime
import random
import string


def test_create_task():
    test_id = uuid.uuid4()
    creation_time = datetime.datetime.now()
    due_time = datetime.datetime(2022, 12, 12)
    owner_id = uuid.uuid4()
    description = "random description"
    done = False

    task = model.Task(
        id=test_id,
        creation_time=creation_time,
        due_time=due_time,
        owner_id=owner_id,
        description=description,
        done=done,
    )
    assert task.id == test_id
    assert task.creation_time == creation_time
    assert task.due_time == due_time
    assert task.owner_id == owner_id
    assert task.description == description
    assert task.done == done


def test_create_task_without_duedate():
    task = model.Task(owner_id=uuid.uuid4())
    assert (
        task.creation_time.date() + datetime.timedelta(days=1) == task.due_time.date()
    )


def test_create_task_with_duedate():
    task = model.Task(owner_id=uuid.uuid4(), due_time=datetime.datetime(2025, 10, 2))
    assert task.due_time == datetime.datetime(2025, 10, 2)


def test_no_ownerid():
    with pytest.raises(Exception):
        task = model.Task()


def test_incorrect_due_time():
    with pytest.raises(Exception):
        task = model.Task(due_time=datetime.datetime(1988, 10, 2))


def test_create_user():
    user_id = uuid.uuid4()
    first_name = "random first name"
    last_name = "random last name"
    password_hash = model.generate_hexdigest("random password")
    user = model.User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        password_hash="random password",
    )
    assert user.id == user_id
    assert user.first_name == user.first_name
    assert user.last_name == user.last_name
    assert user.password_hash == password_hash


def test_no_first_name():
    with pytest.raises(Exception):
        model.User()


def test_no_last_name():
    with pytest.raises(Exception):
        model.User(first_name="random")


def test_no_password():
    with pytest.raises(Exception):
        model.User(first_name="random first name", last_name="random last name")


def test_autheticate_password():
    test_pass = "correct password"
    user = model.User(first_name="ramish", last_name="rasool", password_hash=test_pass)
    assert user.authenticate("correct password")
    assert not user.authenticate("incorrect password")
