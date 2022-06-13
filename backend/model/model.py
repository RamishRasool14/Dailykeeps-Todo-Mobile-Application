from dataclasses import dataclass
import hashlib
import uuid
from datetime import datetime, timedelta

# dataclass documentation https://docs.python.org/3/library/dataclasses.html


def generate_hexdigest(string: str) -> str:  # Assuming string to be in utf-8 format.
    return hashlib.sha256(bytes(string, " utf-8 ")).hexdigest()


@dataclass
class Task:
    """A class containing data for tasks. Using dataclass because they are used for classes that primarily store data"""

    id: uuid = uuid.uuid4()
    creation_time: datetime = datetime.now()
    due_time: datetime = None
    owner_id: uuid = None
    description: str = ""
    done: bool = False

    def __post_init__(self):
        if self.owner_id is None:
            raise Exception("owner id None")

        if self.due_time is None:
            self.due_time = self.creation_time + timedelta(days=1)
        elif self.due_time <= self.creation_time:
            raise Exception("due time cannot be before creation time")


@dataclass
class User:
    """A class containing data for registered User and their Tasks in the system"""

    id: uuid = uuid.uuid4()
    first_name: str = None
    last_name: str = None
    password_hash: str = None

    def __post_init__(self):
        if self.first_name == None:
            raise Exception("first name not initialized")
        elif self.last_name == None:
            raise Exception("last name not initialized")
        if self.password_hash is None:
            raise Exception("password not initialized")
        self.password_hash = generate_hexdigest(self.password_hash)

    def authenticate(self, password: str) -> bool:
        return generate_hexdigest(password) == self.password_hash
