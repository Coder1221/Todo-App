from services.todo.adapters import repository
from services.todo.domain import model as td
import pytest


@pytest.fixture(scope="function")
def todo_object():
    title = "my_title"
    description = "short description"
    status = 2
    user_id = "@#ESWE@"
    created_data_class = td.Todo(user_id, title, description, status)
    return created_data_class


@pytest.fixture(scope="function")
def fake_todo_repository(request):
    repo = repository.FakeTodoRepository()
    request.cls.repo = repo


@pytest.mark.usefixtures("fake_todo_repository", "todo_object")
class TestTodoRepository:
    def test_repo_should_add_todo(self, todo_object):
        self.repo.add(todo_object)
        assert self.repo.get_by_id(todo_object.id).id == todo_object.id

    def test_repo_get_by_id(self, todo_object):
        self.repo.add(todo_object)
        assert self.repo.get_by_id(todo_object.id) == todo_object

    def test_repo_should_update_todo(self, todo_object):
        assert todo_object.title == "my_title"
        todo_object.update_title("NEW TITLE")
        self.repo.save(todo_object)
        assert self.repo.get_by_id(todo_object.id).title == "NEW TITLE"

    def test_repo_should_delete_todo(self, todo_object):
        self.repo.add(todo_object)
        assert self.repo.get_by_id(todo_object.id).id == todo_object.id
        self.repo.delete(todo_object)
        assert self.repo.get_by_id(todo_object.id) == None
