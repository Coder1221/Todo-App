from services.user.domain import model as td
import services.exceptions as errors


def user_login(user_obj: td.User, password: str) -> bool:
    """Checks the user given password with stored password if both are same it will return True else it will raise error"""
    if user_obj.check_password(password):
        return True
    raise errors.LoginFailure
