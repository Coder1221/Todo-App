import jwt
from functools import wraps
from flask import request
from services.user.entrypoints import queries


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
        current_user = queries.authenticate(token=token)
        if current_user is None:
            return {
                "success": False,
                "message": "Token is invalid",
                "data": None,
                "error": "Unauthorized",
            }, 401
        return f(current_user=current_user, *args, **kwargs)

    return decorator
