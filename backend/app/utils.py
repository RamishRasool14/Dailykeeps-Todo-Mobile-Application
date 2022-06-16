import uuid
from model import Task, User
import string
import hashlib
import random
from typing import Optional
from datetime import datetime, timedelta
import uuid

generate_random_string = lambda x: "".join(
    random.choices(string.ascii_uppercase + string.digits, k=x)
)


def create_random_user(id: Optional[str] = None):
    return User(
        id=str(uuid.uuid4()),
        first_name=generate_random_string(5),
        last_name=generate_random_string(5),
        password_hash=generate_random_string(10),
    )


def create_random_task(owner_id: Optional[str] = None):
    return Task(
        id=str(uuid.uuid4()),
        owner_id=owner_id,
        description=generate_random_string(20),
        creation_time=datetime.now(),
    )
