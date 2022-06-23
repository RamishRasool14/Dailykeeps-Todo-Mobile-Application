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
    task = model.Task(
        owner_id=uuid.uuid4(), id=uuid.uuid4(), creation_time=datetime.datetime.now()
    )
    assert (
        task.creation_time.date() + datetime.timedelta(days=1) == task.due_time.date()
    )


def test_create_task_with_duedate():
    task = model.Task(
        owner_id=uuid.uuid4(),
        id=uuid.uuid4(),
        creation_time=datetime.datetime.now(),
        due_time=datetime.datetime(2025, 10, 2),
    )
    assert task.due_time == datetime.datetime(2025, 10, 2)


def test_incorrect_due_time():
    with pytest.raises(model.InvalidDueTime):
        task = model.Task(
            owner_id=1,
            id=uuid.uuid4(),
            creation_time=datetime.datetime.now(),
            due_time=datetime.datetime(1988, 10, 2),
        )


def test_create_user():
    user_id = uuid.uuid4()
    test_first_name = "random first name"
    test_last_name = "random last name"
    email = "ramish_rasool@hotmail.com"
    test_password_hash = model.generate_hexdigest("random password")
    user = model.User(
        first_name=test_first_name,
        last_name=test_last_name,
        password="random password",
        id=user_id,
        email=email,
    )
    assert user.id == user_id
    assert user.first_name == test_first_name
    assert user.last_name == test_last_name
    assert user.password_hash == test_password_hash
    assert user.email == email


def test_autheticate_password():
    test_pass = "correct password"
    user = model.User(
        id=uuid.uuid4(),
        first_name="ramish",
        last_name="rasool",
        email="randomemail@hotmail.com",
        password=test_pass,
    )
    assert user.authenticate("correct password")
    assert not user.authenticate("incorrect password")
