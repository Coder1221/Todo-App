import services.todo.entrypoints.commands as todo_commands
import services.exceptions as errors
import pytest
import services.user.adapters.repository as user_repository
import services.todo.adapters.repository as todo_repository
import services.user.domain.model as user_model
import services.todo.domain.model as todo_model


@pytest.fixture(scope="function")
def user_obj():
    name = "test_name"
    email = "test@tajir-app.com"
    password = "123456"
    created_obj = user_model.User(name, email, password)
    return created_obj


@pytest.fixture(scope="function")
def todo_object():
    title = "my_title"
    description = "short description"
    status = "IN_PROGRESS"
    user_id = ""
    priority = 2
    created_data_class = todo_model.Todo(user_id, title, description, status, priority)
    return created_data_class


def test_todo_creation(user_obj, todo_object):
    user_repo = user_repository.FakeUserRepository()
    todo_repo = todo_repository.FakeTodoRepository()

    r_user = user_repo.add(user_obj)
    saved_todo_id = todo_commands.create_todo(
        r_user.id,
        todo_object.title,
        todo_object.description,
        todo_object.status,
        todo_repo,
    )

    saved_todo = todo_repo.get_by_id(saved_todo_id)
    assert saved_todo.user_id == r_user.id
    assert saved_todo.title == todo_object.title


def test_decrease_priority(user_obj, todo_object):
    user_repo = user_repository.FakeUserRepository()
    todo_repo = todo_repository.FakeTodoRepository()

    r_user = user_repo.add(user_obj)
    todo_object.user_id = r_user.id

    todo_repo.add(todo_object)
    r_todo = todo_repo.get_by_id(todo_object.id)

    todo_commands.decrease_priority(r_todo.id, r_user.id, todo_repo)
    # priority will go from 2 to 1
    todo_commands.decrease_priority(r_todo.id, r_user.id, todo_repo)
    # priority will go from 1 to 0

    with pytest.raises(errors.AlreadyOnLowPriority):
        #  it will raise error as priority can'y go below zero
        todo_commands.decrease_priority(r_todo.id, r_user.id, todo_repo)
