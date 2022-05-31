from services.user.domain import model as td
from services.user.adapters import repository
import uuid


def create_user_account(
    name: str, email: str, password: str, repo: repository.AbstractUserRepository
) -> str:
    """Create a new user account for which then user can login in to application"""
    user_uuid = str(uuid.uuid4())
    user = td.User(id=user_uuid, name=name, email=email, password=password)
    repo.add(user)
    # returning user_uuid because we will need in for testing purpos
    return user_uuid
