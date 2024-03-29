import jwt
from functools import wraps
from flask import request
from services.user.entrypoints import queries
from services.user.adapters.repository import UserRepository
from services.todo.adapters.repository import TodoRepository
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def repo_for_todo():
    conn = psycopg2.connect(
        host=os.getenv("localhost"),
        database=os.getenv("PG_DB_NAME"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
    )
    conn.set_session(autocommit=True)
    return TodoRepository(conn)


def repo_for_user():
    conn = psycopg2.connect(
        host=os.getenv("localhost"),
        database=os.getenv("PG_DB_NAME"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
    )
    conn.set_session(autocommit=True)
    return UserRepository(conn)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return {
                "success": False,
                "message": "Token is missing",
                "data": None,
                "error": "Unauthorized",
            }, 401
        repo = repo_for_user()
        current_user = queries.authenticate_jwt_token(token, repo)
        if current_user is None:
            return {
                "success": False,
                "message": "Token is invalid",
                "data": None,
                "error": "Unauthorized",
            }, 401
        return f(current_user=current_user, *args, **kwargs)

    return decorator
