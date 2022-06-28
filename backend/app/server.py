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

app = Flask(__name__)

if os.getenv("CREATENEWDB") == "1":
    database.Database(False)


@app.route("/", methods=["GET"])
def main_page():
    return "Hello I am working good"


# Payload { "first_name" : , "last_name" : .... " }
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
    except Exception as e:
        print(e)
        return {"description": "failed to register user"}


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
    except Exception as e:
        print(e)
        return {"description": "failed to log in user"}


# Payload {"owner_id": "b8000698-86c3-4f0f-86ad-6f5c44986b2e", "description": "a different task"}
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
        print(e)
        return {"description": "failed to add task"}


# Payload {"owner_id": "b8000698-86c3-4f0f-86ad-6f5c44986b2e", "day":"2022-06-21"}
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
    except Exception as e:
        print(e)
        return {"description": "failed to get task"}


# Payload {"id": "0eef391b-8eb0-4f4d-b23d-79051f7e51e5", "due_time": "", "done": "true", "description": "edited task"}
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
        print(e)
        return {"description": "failed to edit task"}


@app.route("/delete_task", methods=["POST"])
def delete_task():
    try:
        data = request.json
        user_id = utils.jwt_decode(data["token"])
        task_repo = TaskRepository()
        task_repo.delete(user_id)
        return {"description": "successfully deleted"}
    except Exception as e:
        print(e)
        return {"description": "failed to delete task"}
