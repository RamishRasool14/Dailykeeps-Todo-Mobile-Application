from dataclasses import dataclass
import hashlib
import uuid
from datetime import datetime, timedelta

# dataclass documentation https://docs.python.org/3/library/dataclasses.html


def generate_hexdigest(string: str) -> str:  # Assuming string to be in utf-8 format.
    return hashlib.sha256(bytes(string, " utf-8 ")).hexdigest()


class OwneridNotFoundException(Exception):
    pass


class InvalidDueTime(Exception):
    pass


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
            raise OwneridNotFoundException

        if self.due_time is None:
            self.due_time = self.creation_time + timedelta(days=1)
        elif self.due_time <= self.creation_time:
            raise InvalidDueTime


@dataclass
class User:
    """A class containing data for registered User and their Tasks in the system"""

    first_name: str
    last_name: str
    password_hash: str
    id: uuid = uuid.uuid4()

    def __post_init__(self):
        self.password_hash = generate_hexdigest(self.password_hash)

    def authenticate(self, password: str) -> bool:
        return generate_hexdigest(password) == self.password_hash
