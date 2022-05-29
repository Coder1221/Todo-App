from backend.services.user.domain import model as td
from backend.services.user.adapters import repository


def create_user_account(
    name: str, email: str, password: str, repo: repository.AbstractUserRepository
) -> None:
    """Create a new user account for which then user can login in to application"""
    user = td.User(name=name, email=email, password=password)
    repo.add(user)
