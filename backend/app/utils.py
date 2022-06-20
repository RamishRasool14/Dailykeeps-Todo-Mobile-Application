import uuid
from model import Task, User
import string
import hashlib
import random
from typing import Optional
from datetime import datetime, timedelta
import uuid
import jwt
import config

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


def jwt_decode(data):
    return data
    return jwt.decode(
        data, bytes(config.JWTSECRET.encode("utf-8")), algorithms=["HS256"]
    )


def jwt_encode(data):
    return data
    return jwt.encode(data, bytes(config.JWTSECRET.encode("utf-8")), algorithm="HS256")
