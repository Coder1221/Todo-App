import pytest
import services.user.entrypoints.commands as user_commands
import services.user.domain.model as td
import services.user.adapters.repository as repository
import uuid


def test_create_user_account():
    fake_repo = repository.FakeUserRepository()
    user_uuid = user_commands.create_user_account(
        "TEST USER", "TEST@GMAIL.COM", "123456", fake_repo
    )

    r_user = fake_repo.get_by_id(user_uuid)

    assert r_user.email == "TEST@GMAIL.COM"
    assert r_user.check_password("123456"), True
