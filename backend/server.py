from flask import Flask, request
import jwt
from functools import wraps
from services.user.entrypoints import queries as user_queries
from services.user.entrypoints import commands as user_commands
from services.todo.entrypoints import queries as todo_queries
from services.todo.entrypoints import commands as todo_commands
from services.user.adapters.repository import UserRepository
from middleware import token_required, repo_for_todo, repo_for_user
import services.exceptions as errors

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Flask server by Tajir<h1>"


@app.route("/login")
def login():
    body_json = request.json
    email = body_json["email"]
    password = body_json["password"]
    repo = repo_for_user()
    try:
        jwt_token = user_queries.user_jwt_token(email, password, repo)
        return {
            "success": True,
            "message": "Successfull login",
            "token": jwt_token,
        }
    except Exception as e:
        return {"success": False, "message": str(e), "token": ""}


@app.route("/signup", methods=["POST"])
def user_signup():
    body_json = request.json
    name = body_json["name"]
    email = body_json["email"]
    password = body_json["password"]
    try:
        user = user_commands.create_user_account(name, email, password, repo_for_user())
        return {
            "success": True,
            "message": "Account created successfully",
            "data": user,
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/todo/date/<date>", methods=["GET"])
@token_required
def all_todos_of_that_date(current_user, date):
    try:
        todos = todo_commands.all_todos_of_certain_date(
            current_user.id, date, repo_for_todo()
        )
        return {"success": True, "data": todos if todos else []}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/todos", methods=["POST"])
@token_required
def create_todo(current_user):
    try:
        body_json = request.json
        try:
            title = body_json["title"]
            description = body_json["description"]
            status = body_json["status"]
        except:
            raise errors.TodoAttributeMissingError(
                "Requested body is missing attributes for todo"
            )

        todo = todo_commands.create_todo(
            current_user.id, title, description, status, repo=repo_for_todo()
        )
        return {"success": True, "message": "Todo created successfully", "data": todo}
    except Exception as e:
        return {"success": False, "message": str(e), "data": []}


@app.route("/todo/<uuid>/increase_priority", methods=["POST"])
@token_required
def increase_priority(current_user, uuid):
    try:
        todo_commands.increase_priority(uuid, current_user.id, repo_for_todo())
        return {"success": True, "message": "Priority increased successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/todo/<uuid>/decrease_priority", methods=["POST"])
@token_required
def decrease_priority(current_user, uuid):
    try:
        todo_commands.decrease_priority(uuid, current_user.id, repo_for_todo())
        return {"success": True, "message": "Priority decreased successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route("/todo/<uuid>", methods=["DELETE"])
@token_required
def delete_todo(current_user, uuid):
    try:
        todo_commands.delete_todo(uuid, repo_for_todo())
        return {"success": True, "message": "Todo deleted successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
