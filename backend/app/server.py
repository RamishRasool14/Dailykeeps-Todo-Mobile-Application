from datetime import datetime
from uuid import uuid4
import json
from flask import Flask, request, jsonify
from repository import TaskRepository, UserRepository
from model import User, Task
import utils
import database
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
if os.getenv("CREATENEWDB") == "1":
    database.Database(existing_db=False)

app = Flask(__name__)

# Payload { "user": { "first_name" : , "last_name" : .... " } }
@app.route("/register_user", methods=["POST"])
def register():
    data = request.json
    data = utils.jwt_decode(data)["user"]
    try:
        user = User(
            id=uuid4(),
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
        )
        user_repo = UserRepository()
        user_repo.add(user)
        return utils.jwt_encode({"description": "successfully registered user"})
    except Exception as e:
        print(e)
        return utils.jwt_encode({"description": "failed to register user"})


# Payload {"user": {"first_name": "Ramish", "last_name": "Rasool", "email": "ramishrasool@hotmail.com", "password": "iloveanime"} }
@app.route("/login", methods=["GET"])
def login():
    data = request.json
    data = utils.jwt_decode(data)["user"]
    try:
        user_repo = UserRepository()
        user = user_repo.get(by="email", id=data["email"])
        assert user.authenticate(data["password"])
        return utils.jwt_encode(
            {"description": "successfully logged in", "user": {"id": user.id}}
        )
    except Exception as e:
        print(e)
        return utils.jwt_encode({"description": "failed to log in user"})


# Payload {"task": {"owner_id": "b8000698-86c3-4f0f-86ad-6f5c44986b2e", "description": "a different task"} }
@app.route("/create_task", methods=["POST"])
def create_task():
    data = request.json
    data = utils.jwt_decode(data)["task"]
    try:
        task_repo = TaskRepository()
        task = Task(
            owner_id=data["owner_id"],
            id=str(uuid4()),
            creation_time=datetime.now(),
            description=data["description"],
        )
        task_repo.add(task)
        return utils.jwt_encode({"description": "successfully added task"})
    except Exception as e:
        print(e)
        return utils.jwt_encode({"description": "failed to add task"})


# Payload {"task": {"owner_id": "b8000698-86c3-4f0f-86ad-6f5c44986b2e", "day":"2022-06-21"} }
@app.route("/get_task", methods=["GET"])
def get_task():
    data = request.json
    data = utils.jwt_decode(data)["task"]
    try:
        task_repo = TaskRepository()
        if data["day"]:
            tasks = task_repo.get_task_for_a_day(data["owner_id"], data["day"])
        else:
            tasks = task_repo.get(data["owner_id"])
        return utils.jwt_encode({"description": "successfull", "data": tasks})
    except Exception as e:
        print(e)
        return utils.jwt_encode({"description": "failed to get task"})


# Payload {"task": {"id": "0eef391b-8eb0-4f4d-b23d-79051f7e51e5", "due_time": "", "done": "true", "description": "edited task"} }
@app.route("/edit_task", methods=["POST"])
def edit_task():
    data = request.json
    data = utils.jwt_decode(data)["task"]
    try:
        task_repo = TaskRepository()
        original_task = task_repo.get_by_id(data["id"])

        if data["due_time"]:
            due_time = datetime.strptime(data["due_time"], "%Y-%m-%d")

        else:
            due_time = original_task.due_time

        if data["done"]:
            done = data["done"]
        else:
            done = original_task.done

        if data["description"]:
            description = data["description"]
        else:
            description = original_task.description

        edited_task = Task(
            id=data["id"],
            creation_time=original_task.creation_time,
            owner_id=original_task.owner_id,
            due_time=due_time,
            done=done,
            description=description,
        )
        task_repo.update(edited_task)
        return utils.jwt_encode({"description": "successfully updated"})
    except Exception as e:
        print(e)
        return utils.jwt_encode({"description": "failed to edit task"})


@app.route("/delete_task", methods=["GET"])
def delete_task():
    data = request.json
    data = utils.jwt_decode(data)["task"]
    try:
        task_repo = TaskRepository()
        task_repo.delete(data["id"])
        return utils.jwt_encode({"description": "successfully deleted"})
    except Exception as e:
        print(e)
        return utils.jwt_encode({"description": "failed to delete task"})
