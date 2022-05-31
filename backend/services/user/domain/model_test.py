import services.user.domain.model as td
import pytest


@pytest.fixture(scope="function")
def user_obj():
    name = "test_name"
    email = "test@tajir-app.com"
    password = "123456"
    created_obj = td.User(name, email, password)
    return created_obj


def test_check_pasword(user_obj):
    assert user_obj.check_password("123456") == True
    assert user_obj.check_password("12345") == False
    assert user_obj.check_password("-123456") == False


def test_encrypt_password(user_obj):
    assert (
        user_obj.encrypt_password("123")
        == "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
    )
