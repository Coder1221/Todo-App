import pytest
import services.user.domain.model as td
import services.user.adapters.repository as repository


@pytest.fixture(scope="function")
def user_obj():
    return td.User(name="Test User", email="tet@tajir.com", password="12345")


@pytest.fixture(scope="function")
def fake_user_repository(request):
    repo = repository.FakeUserRepository()
    request.cls.repo = repo


@pytest.mark.usefixtures("fake_user_repository", "user_obj")
class TestUserRepository:
    def test_repo_create_user(self, user_obj):
        self.repo.add(user_obj)
        assert self.repo.get_by_id(user_obj.id).id == user_obj.id

    def test_repo_get_by_id(self, user_obj):
        self.repo.add(user_obj)
        assert self.repo.get_by_id(user_obj.id).id == user_obj.id

    def test_repo_should_update(self, user_obj):
        assert user_obj.name == "Test User"
        user_obj.update_name("Updated Name")
        assert user_obj.name == "Updated Name"
        self.repo.save(user_obj)
        assert self.repo.get_by_id(user_obj.id).name == "Updated Name"

    def test_repo_should_should_delete_user(self, user_obj):
        self.repo.add(user_obj)
        assert self.repo.get_by_id(user_obj.id).id == user_obj.id
        self.repo.delete(user_obj)
        assert self.repo.get_by_id(user_obj.id) == None

    def test_user_passwords_are_note_stored_in_plain_text(self, user_obj):
        self.repo.add(user_obj)
        assert self.repo.get_by_id(user_obj.id).password != "12345"
        assert (
            self.repo.get_by_id(user_obj.id).encrypted_password
            == "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5"
        )
