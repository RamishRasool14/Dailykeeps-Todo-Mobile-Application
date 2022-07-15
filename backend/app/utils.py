import uuid
from model import Task, User
from repository import TaskRepository
import string
import hashlib
import random
from typing import Optional
from datetime import datetime, timedelta
import uuid
import jwt
import time
import os

generate_random_string = lambda x: "".join(
    random.choices(string.ascii_uppercase + string.digits, k=x)
)


def generate_hexdigest(string: str) -> str:  # Assuming string to be in utf-8 format.
    return hashlib.sha256(bytes(string, " utf-8 ")).hexdigest()


def create_random_user(id: Optional[str] = None):
    return User(
        id=str(uuid.uuid4()),
        first_name=generate_random_string(5),
        last_name=generate_random_string(5),
        password=generate_random_string(10),
        email=generate_random_string(15),
    )


def create_random_task(owner_id: Optional[str] = None):
    return Task(
        id=str(uuid.uuid4()),
        owner_id=owner_id,
        description=generate_random_string(20),
        creation_time=datetime.now(),
    )


def make_task_from_json_payload(data):
    task_repo = TaskRepository()
    original_task = task_repo.get_by_id(data["id"])

    if data["due_time"]:
        due_time = datetime.strptime(data["due_time"], "%a, %d %b %Y %H:%M:%S")
    else:
        due_time = original_task.due_time

    if data["done"]:
        done = data["done"]
    else:
        done = original_task.done

    if data["description"]:
        description = data["description"]
    else:
        description = original_task.description

    edited_task = Task(
        id=data["id"],
        creation_time=original_task.creation_time,
        owner_id=original_task.owner_id,
        due_time=due_time,
        done=done,
        description=description,
    )
    return edited_task


def jwt_decode(token):
    decode = jwt.decode(
        token,
        bytes(os.getenv("JWTSECRET").encode("utf-8")),
        algorithms=["HS256"],
    )["user_id"]
    return str(decode)


def jwt_encode(user_id):
    encode = jwt.encode(
        {"user_id": user_id},
        bytes(os.getenv("JWTSECRET").encode("utf-8")),
        algorithm="HS256",
    )
    return encode
