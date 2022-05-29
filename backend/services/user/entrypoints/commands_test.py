import pytest
import backend.services.user.entrypoints.commands as user_commands
import backend.services.user.domain.model as td
import backend.services.user.adapters.repository as repository


def test_create_user_account():
    fake_repo = repository.FakeUserRepository()
    r_user = user_commands.create_user_account(
        "TEST USER", "TEST@GMAIL.COM", "123456", fake_repo
    )
    assert r_user.email == "TEST@GMAIL.COM"
    assert r_user.check_password("123456"), True
