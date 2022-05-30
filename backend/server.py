from flask import Flask, request
import jwt
from functools import wraps
import sys


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


if __name__ == "__main__":
    app.run(debug=True, host="localhost")
