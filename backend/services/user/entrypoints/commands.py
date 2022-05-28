from services.user.domain import model as td
from services.user.domain import repository


def create_user(
    name: str, email: str, password: str, repo: repository.AbstractUserRepository
):
    user = td.User(name=name, email=email, password=password)
    repo.add(user)

    return ""


def user_signup(self, *args, **kwargs):
    submitted_data = kwargs["data"]
    user_obj = td.User(
        name=submitted_data["name"],
        email=submitted_data["email"],
        password=submitted_data["password"],
    )
    repo = _repo_for_user()
    crearted_obj = repo.add(user_obj)
    if crearted_obj:
        return {
            "success": True,
            "message": "Account crearted successfully",
            "data": crearted_obj,
        }
