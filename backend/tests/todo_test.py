import pytest
from todo import model as td


@pytest.fixture(scope="class")
def todo_object():
    uuid = "2w1jdsj21@3"
    title = "my_title"
    description = "short description"
    status = 2
    created_data_class = td.Todo(uuid, title, description, status, None, None, None)
    return created_data_class


def test_todo_creation(todo_object):
    assert todo_object.uuid == "2w1jdsj21@3"
    assert todo_object.title == "my_title"
    assert todo_object.description == "short description"
    assert todo_object.status == 2


def test_update_status(todo_object):
    # status should not be updated when stored status is same as given
    with pytest.raises(Exception) as e:
        todo_object.update_status("IN_PROGRESS")

    # status should not be updated
    with pytest.raises(KeyError) as e:
        todo_object.update_status("IN_validValue")

    # status shoud be updated by providing enum value
    todo_object.update_status("CLOSED")
    assert todo_object.status == 3


def test_update_title(todo_object):
    prev_title = todo_object.title
    assert todo_object.update_title("My new Title"), True
    assert todo_object.title != prev_title
    assert todo_object.title == "My new Title"


def test_update_description(todo_object):
    prev_description = todo_object.description
    assert todo_object.update_description("My new Description"), True
    assert todo_object.description != prev_description
    assert todo_object.description == "My new Description"
