from flask import Flask, request
import jwt
from functools import wraps
from services.user.entrypoints import queries as user_queries
from services.user.entrypoints import commands as user_commands
from services.todo.entrypoints import queries as todo_queries
from services.todo.entrypoints import commands as todo_commands

from middleware import token_required
import services.exceptions as errors

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Flask server by Tajir<h1>"


@app.route("/login")
def login():
    body_json = request.json
    try:
        jwt_token = user_queries.user_jwt_token(
            email=body_json["email"], password=body_json["password"]
        )
        return {
            "success": True,
            "message": "Successfull login",
            "token": jwt_token,
        }
    except errors.LoginFailure:
        return {"success": False, "message": "Wrong credentials", "token": ""}


# @app.route("/signup", methods=["POST"])
# def user_signup():
#     data = request.json
#     email = data["email"]
#     name = data["name"]
#     password = data["password"]
#     # repo pass
#     user_commands.create_user_account(name, email, password, repo)


# create todo
# @app.route("/todo", methods=["POST"])
# @token_required
# def todo_post(current_user):
#     data = request.json
#     title = data["title"]
#     description = data["description"]
#     status = data["status"]

#     todo_commands.create_todo(current_user.id, title, description, status, repo)


# get or update todo by uuid
# @app.route("/todo/<uuid>", methods=["GET", "PUT"])
# @token_required
# def todo_by_uiid(current_user, uuid):
#     if request.method == "GET":
#         TodoInteractor.get_todo_by_uuid(current_user=current_user, uuid=uuid)
#     elif request.method == "PUT":
#         TodoInteractor.update_todo(current_user=current_user, data=request.json)


# @app.route("/todo/date/<date>", methods=["GET"])
# @token_required
# def all_todos_of_that_date(current_user, date):
#     repo = repo.all_todos_of_that_date(current_user=current_user, date=date)


# @app.route("/todo/increase_priority/<uuid>", methods=["POST"])
# @token_required
# def increase_priority_of_todo(current_user, uuid):
#     todo_commands.increase_priority(uuid, current_user.id)


# @app.route("/todo/decrease_priority/<uuid>", methods=["POST"])
# @token_required
# def decrease_priority_of_todo(current_user, uuid):
#     todo_commands.decrease_priority(uuid, current_user.id)


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
