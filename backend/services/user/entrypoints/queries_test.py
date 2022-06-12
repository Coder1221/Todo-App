import services.user.domain.model as td
import pytest
import services.user.entrypoints.queries as user_queries
import services.exceptions as errors
import services.user.adapters.repository as repository


@pytest.fixture(scope="function")
def user_obj():
    name = "test_name"
    email = "test@tajir-app.com"
    password = "123456"
    created_obj = td.User(name, email, password)
    return created_obj


def test_user_login(user_obj):
    assert user_queries.user_login(user_obj, "123456") == True

    with pytest.raises(errors.LoginFailure):
        user_queries.user_login(user_obj, "12345")


def test_user_jwt_token(user_obj):
    fake_repo = repository.FakeUserRepository()
    fake_repo.add(user_obj)
    assert (
        user_queries.user_jwt_token("test@tajir-app.com", "123456", fake_repo) != None
    )
    with pytest.raises(errors.UserNotFound):
        user_queries.user_jwt_token("testtest@tajir-app.com", "12345", fake_repo)


def test_authenticate_jwt_token(user_obj):
    fake_repo = repository.FakeUserRepository()
    fake_repo.add(user_obj)
    token = user_queries.user_jwt_token("test@tajir-app.com", "123456", fake_repo)
    assert user_queries.authenticate_jwt_token(token, fake_repo).email == user_obj.email
    fake_repo.delete(fake_repo.get_by_email("test@tajir-app.com"))
    with pytest.raises(errors.InvalidJwtToken):
        user_queries.authenticate_jwt_token(token, fake_repo).email == user_obj.email
