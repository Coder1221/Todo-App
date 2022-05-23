from repository import user_repository
import pytest
from models.user import model as td


@pytest.fixture(scope="class")
def user_obj():
    return td.User(name="Test User", email="tet@tajir.com", password="12345")


@pytest.fixture(scope="class")
def fake_user_repository(request):
    repo = user_repository.FakeUserRepository()
    request.cls.repo = repo


@pytest.mark.usefixtures("fake_user_repository", "user_obj")
class TestUserRepository:
    def test_repo_create_user(self, user_obj):
        self.repo.add(user_obj)
        assert self.repo.get_by_id(user_obj.id).id == user_obj.id

    def test_repo_get_by_id(self, user_obj):
        r_obj = self.repo.get_by_id(user_obj.id)
        assert r_obj.id == user_obj.id

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
