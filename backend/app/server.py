from datetime import datetime
from uuid import uuid4
import json
from flask import Flask, request, jsonify
from repository import TaskRepository, UserRepository
from model import User, Task
import exception
import utils
import database
from datetime import datetime
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)

if os.getenv("CREATENEWDB") == "1":
    database.Database(False)


@app.route("/", methods=["GET"])
def main_page():
    return "Hello I am working good"


# Payload { "first_name" : , "last_name" : .... ", "password": ... }
@app.route("/register_user", methods=["POST"])
def register():
    try:
        data = request.json
        user = User(
            id=uuid4(),
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
        )
        user_repo = UserRepository()
        user_repo.add(user)
        return {"description": "successfully registered user"}
    except Exception:
        raise exception.ErrorRegisteringUser()


# Payload {"first_name": "Ramish", "last_name": "Rasool", "email": "ramishrasool@hotmail.com", "password": "iloveanime"}
@app.route("/login_user", methods=["POST"])
def login_user():
    try:
        data = request.json
        user_repo = UserRepository()
        user = user_repo.get(by="email", id=data["email"])
        assert user.authenticate(data["password"])
        return {
            "description": "successfully logged in",
            "token": utils.jwt_encode(user.id),
        }
    except Exception:
        raise exception.ErrorLoggingIn()


# Payload {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNmQwNmIzNmYtNGE1MS00YTExLTk5ZjAtYzAxMzQxZjEyMjgyIn0._nPQYfmO2jJM8XycGQUPUZ9V26uJMta3Oi9pgHxjucI", "description": "a different task"}
@app.route("/create_task", methods=["POST"])
def create_task():
    try:
        data = request.json
        user_id = utils.jwt_decode(data["token"])
        task_repo = TaskRepository()
        task = Task(
            owner_id=user_id,
            id=str(uuid4()),
            creation_time=datetime.now(),
            description=data["description"],
        )
        task_repo.add(task)
        return {"description": "successfully added task"}
    except Exception as e:
        raise exception.ErrorCreatingTask(e)


# Payload {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNmQwNmIzNmYtNGE1MS00YTExLTk5ZjAtYzAxMzQxZjEyMjgyIn0._nPQYfmO2jJM8XycGQUPUZ9V26uJMta3Oi9pgHxjucI", "day":"" }
@app.route("/get_task", methods=["POST"])
def get_task():
    try:
        data = request.json
        user_id = utils.jwt_decode(data["token"])
        task_repo = TaskRepository()
        if data["day"]:
            tasks = task_repo.get_task_for_a_day(user_id, data["day"])
        else:
            tasks = task_repo.get(user_id)
        return {"description": "successfull", "data": tasks}
    except Exception:
        raise exception.ErrorGettingTask()


# Payload {"due_time": "2025-05-25","done": "true", "description": "edited task I am",    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWQwOTMzZDYtZjYzMi00NWVkLWJiY2ItM2NlM2Y5YmVhNjFiIn0.7RS3oVLHoqlB8o0n09idcKn8rnBJ0SAhPGV8KCFjcBU",    "id":"bda7283b-9df6-477e-a5b0-6f6c8183e310"}
@app.route("/edit_task", methods=["POST"])
def edit_task():
    try:
        data = request.json
        user_id = utils.jwt_decode(data["token"])
        task_repo = TaskRepository()
        edited_task = utils.make_task_from_json_payload(data)
        task_repo.update(edited_task)
        return {"description": "successfully updated"}
    except Exception as e:
        raise exception.ErrorEditingTask(e)


# Payload {"id":"bda7283b-9df6-477e-a5b0-6f6c8183e310"}
@app.route("/delete_task", methods=["POST"])
def delete_task():
    try:
        data = request.json
        user_id = data["id"]

        task_repo = TaskRepository()
        task_repo.delete(user_id)
        return {"description": "successfully deleted"}
    except Exception:
        raise exception.ErrorDeletingTask()
