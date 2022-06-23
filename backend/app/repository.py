from abc import ABC, abstractmethod
from database import Database
from model import User, Task
from typing import Optional, Union
import exception


class ABClass(ABC):
    @abstractmethod
    def get(self, id: str):
        pass

    @abstractmethod
    def add(self, model: Union[Task, User]):
        pass

    @abstractmethod
    def update(self, model: Union[Task, User]):
        pass

    @abstractmethod
    def delete(self, id: str):
        pass


class UserRepository(ABClass):
    def get(self, id: Optional[str] = None, by: Optional[set] = "id", all=False):
        with Database() as db:
            cur = db.execute('select * from "user" where "{}"=%s'.format(by), id)
            user = cur.fetchone()
            if not user:
                raise exception.UserNotFound()
            return User(
                id=user[0],
                first_name=user[1],
                last_name=user[2],
                email=user[3],
                password_hash=user[4],
                password=None,
            )

    def add(self, user: User):
        with Database() as db:
            db.execute(
                'insert into "user" (id, first_name, last_name, email,password) values (%s,%s,%s,%s,%s)',
                str(user.id),
                user.first_name,
                user.last_name,
                user.email,
                user.password_hash,
            )
            db.commit()

    def update(self, user: User):
        with Database() as db:
            db.execute(
                'update "user" set first_name=%s, last_name=%s, password=%s where id=%s',
                user.first_name,
                user.last_name,
                user.password_hash,
                user.id,
            )
            db.commit()

    def delete(self, id: str):
        with Database() as db:
            db.execute(
                'delete from "user" where id=%s',
                id,
            )
            db.commit()


class TaskRepository(ABClass):
    def get(self, id: str):
        with Database() as db:
            cur = db.execute(f'select * from "task" where "owner_id"=%s ', id)
            tasks = cur.fetchall()
            task_objs = []
            for task in tasks:
                task_objs.append(
                    Task(
                        id=task[0],
                        creation_time=task[1],
                        due_time=task[2],
                        owner_id=task[3],
                        description=task[4],
                        done=task[5],
                    )
                )
            return task_objs

    def get_by_id(self, id):
        with Database() as db:
            cur = db.execute(f'select * from "task" where "id"=%s ', id)
            task = cur.fetchone()
            if task:
                get_task = Task(
                    id=task[0],
                    creation_time=task[1],
                    due_time=task[2],
                    owner_id=task[3],
                    description=task[4],
                    done=task[5],
                )
                return get_task
            else:
                return None

    def get_task_for_a_day(self, id, date):
        with Database() as db:
            cur = db.execute(
                f'select * from "task" where "owner_id"=%s and date("due_time")=%s ',
                id,
                date,
            )
            tasks = cur.fetchall()
            task_objs = []
            for task in tasks:
                task_objs.append(
                    Task(
                        id=task[0],
                        creation_time=task[1],
                        due_time=task[2],
                        owner_id=task[3],
                        description=task[4],
                        done=task[5],
                    )
                )
            return task_objs

    def add(self, task: Task):
        with Database() as db:
            db.execute(
                'insert into "task" (id, creation_time, due_time, owner_id, description, done) values (%s,%s,%s,%s,%s,%s)',
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
                'update "task" set due_time=%s, description=%s, done=%s where id=%s',
                task.due_time,
                task.description,
                task.done,
                task.id,
            )
            db.commit()

    def delete(self, id: str):
        with Database() as db:
            db.execute(
                'delete from "task" where id=%s',
                id,
            )
            db.commit()
