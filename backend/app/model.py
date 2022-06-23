from dataclasses import dataclass
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Optional

# dataclass documentation https://docs.python.org/3/library/dataclasses.html


def generate_hexdigest(string: str) -> str:  # Assuming string to be in utf-8 format.
    return hashlib.sha256(bytes(string, " utf-8 ")).hexdigest()


class InvalidDueTime(Exception):
    pass


@dataclass
class Task:
    """A class containing data for tasks. Using dataclass because they are used for classes that primarily store data"""

    owner_id: str
    id: str
    creation_time: datetime
    description: Optional[str] = ""
    done: bool = False
    due_time: Optional[datetime] = None

    def __post_init__(self):
        if not self.due_time:
            self.due_time = self.creation_time + timedelta(days=1)
        elif self.due_time <= self.creation_time:
            raise InvalidDueTime


@dataclass
class User:
    """A class containing data for registered User and their Tasks in the system"""

    id: str
    first_name: str
    last_name: str
    password: str
    email: str
    password_hash: str = None

    def __post_init__(self):
        if self.password:
            self.password_hash = generate_hexdigest(self.password)

    def authenticate(self, password: str) -> bool:
        return generate_hexdigest(password) == self.password_hash
