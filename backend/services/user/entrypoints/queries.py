from services.user.domain import model
from services.user.adapters import repository
import jwt
from services.user.entrypoints import queries
import services.exceptions as errors
from typing import Optional


def user_login(user_obj: model.User, password: str) -> bool:
    """Checks the user given password with stored password if both are same it will return True else it will raise error"""
    if user_obj.check_password(password):
        return True
    raise errors.LoginFailure


def authenticate_jwt_token(
    token: str, repo: repository.AbstractUserRepository
) -> model.User:
    """Authenticates the given token and it will return user object based on the decoded token id"""
    data = jwt.decode(token, "some_secret", algorithms=["HS256"])
    current_user = repo.get_by_id(data["user_id"])
    if not current_user:
        raise errors.InvalidJwtToken
    return current_user


def user_jwt_token(
    email: str, password: str, repo: repository.AbstractUserRepository
) -> Optional[str]:
    """Returns the jwt token for the given email and password if both are correct"""
    jwt_secret = "some_secret"
    jwt_algorithum = "HS256"

    r_user_obj = repo.get_by_email(email)
    if r_user_obj:
        can_login = queries.user_login(r_user_obj, password)
        payload = {"user_id": r_user_obj.id}
        jwt_token = jwt.encode(payload, jwt_secret, jwt_algorithum)
        return jwt_token
    else:
        raise errors.UserNotFound("User not found")
