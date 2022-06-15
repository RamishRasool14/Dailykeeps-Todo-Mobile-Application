from model import Task, User
import string
import hashlib
import random
from typing import Optional
from datetime import datetime, timedelta

generate_random_string = lambda x: "".join(
    random.choices(string.ascii_uppercase + string.digits, k=x)
)


def create_random_user(id: Optional[str] = None):
    return User(
        id=id,
        first_name=generate_random_string(5),
        last_name=generate_random_string(5),
        password_hash=generate_random_string(10),
    )


def create_random_task(id: Optional[str] = None):
    return Task(
        id=id,
        creation_time=datetime.now(),
        due_time=datetime.now()+timedelta(days = 1)
        first_name=generate_random_string(5),
        last_name=generate_random_string(5),
        password_hash=generate_random_string(10),
    )
