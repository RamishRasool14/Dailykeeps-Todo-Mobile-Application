from ctypes import util
from uuid import uuid4
from database import Database
import repository
import psycopg2
import pytest
import utils


def test_database_connect():
    print("\nConnecting to the PostgreSQL database...")
    db = Database()
    db.connect()
    print("PostgreSQL database version:")
    cur = db.execute("SELECT version()")
    db_version = cur.fetchone()
    print(db_version)
    print("Connected Successfully")


user = repository.UserRepository()
# print(utils.create_random_user())
# user.create(utils.create_random_user())

# user.create(utils.create_random_user())

# user.create(
#     utils.User(id="fix", first_name="abc", last_name="xsc", password_hash="asdf")
# )
# user.update(utils.create_random_user(id="fix"))
# user.delete("fix")
print(user.get(all=True))
