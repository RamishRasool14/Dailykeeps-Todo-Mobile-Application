from abc import ABC, abstractmethod
from database import Database, DuplicateError
from model import User, Task
from typing import Optional


class ABClass(ABC):
    def __init__(self, table):
        self.table = table

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


class UserRepository(ABClass):
    def __init__(self):
        super().__init__("user")

    def get(self, id: Optional[str] = None, all=False):
        with Database() as db:
            cur = db.execute(f'select * from "{self.table}" where "id"=%s ', id)
            if all:
                cur = db.execute(f'select * from "{self.table}"')

            return cur.fetchall()

    def create(self, user: User):
        with Database() as db:
            db.execute(
                'insert into "{}" (id, first_name, last_name, password) values (%s,%s,%s,%s)'.format(
                    self.table
                ),
                str(user.id),
                user.first_name,
                user.last_name,
                user.password_hash,
            )
            db.commit()

    def update(self, user: User):
        with Database() as db:
            db.execute(
                'update "{}" SET first_name=%s, last_name=%s, password=%s where id=%s'.format(
                    self.table
                ),
                user.first_name,
                user.last_name,
                user.password_hash,
                user.id,
            )
            db.commit()

    def delete(self, id: str):
        with Database() as db:
            db.execute(
                'delete from "{}" where id=%s'.format(self.table),
                id,
            )
            db.commit()


class TaskRepository(ABClass):
    def __init__(self):
        super().__init__("task")

    def get(self, id: Optional[str] = None, all=False):
        with Database() as db:
            cur = db.execute(f'select * from "{self.table}" where "id"=%s ', id)
            if all:
                cur = db.execute(f'select * from "{self.table}"')

            return cur.fetchall()

    def create(self, user: User):
        with Database() as db:
            db.execute(
                'insert into "{}" (id, first_name, last_name, password) values (%s,%s,%s,%s)'.format(
                    self.table
                ),
                str(user.id),
                user.first_name,
                user.last_name,
                user.password_hash,
            )
            db.commit()

    def update(self, user: User):
        with Database() as db:
            db.execute(
                'update "{}" SET first_name=%s, last_name=%s, password=%s where id=%s'.format(
                    self.table
                ),
                user.first_name,
                user.last_name,
                user.password_hash,
                user.id,
            )
            db.commit()

    def delete(self, id: str):
        with Database() as db:
            db.execute(
                'delete from "{}" where id=%s'.format(self.table),
                id,
            )
            db.commit()
