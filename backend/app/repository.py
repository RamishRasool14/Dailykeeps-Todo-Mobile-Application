from abc import ABC, abstractmethod
from database import Database
from model import User, Task
from typing import Optional
import exception


class ABClass(ABC):
    def __init__(self, table):
        self.table = table

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def add(self, *args, **kwargs):
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
            user = cur.fetchone()
            if user is None:
                raise exception.UserNotFound()
            return User(
                id=user[0],
                first_name=user[1],
                last_name=user[2],
                password_hash=user[3],
                generate_hash=False,
            )

    def add(self, user: User):
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
                'update "{}" set first_name=%s, last_name=%s, password=%s where id=%s'.format(
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
            cur = db.execute(f'select * from "{self.table}" where "owner_id"=%s ', id)
            return [
                Task(
                    id=task[0],
                    creation_time=task[1],
                    due_time=task[2],
                    owner_id=task[3],
                    description=task[4],
                    done=task[5],
                )
                for task in cur.fetchall()
            ]

    def add(self, task: Task):
        with Database() as db:
            db.execute(
                'insert into "{}" (id, creation_time, due_time, owner_id, description, done) values (%s,%s,%s,%s,%s,%s)'.format(
                    self.table
                ),
                task.id,
                task.creation_time,
                task.due_time,
                task.owner_id,
                task.description,
                task.done,
            )
            db.commit()

    def update(self, task: Task):
        with Database() as db:
            db.execute(
                'update "{}" SET due_time=%s, description=%s, done=%s where id=%s'.format(
                    self.table
                ),
                task.due_time,
                task.description,
                task.done,
                task.id,
            )
            db.commit()

    def delete(self, id: str):
        with Database() as db:
            db.execute(
                'delete from "{}" where id=%s'.format(self.table),
                id,
            )
            db.commit()
