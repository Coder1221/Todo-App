import pytest
from models.todo import model as td


@pytest.fixture(scope="class")
def todo_object():
    title = "my_title"
    description = "short description"
    status = 2
    user_id = "@#ESWE@"
    created_data_class = td.Todo(
        user_id, title, description, status
    )
    return created_data_class


def test_todo_creation(todo_object):
    assert todo_object.title == "my_title"
    assert todo_object.description == "short description"
    assert todo_object.status == 2
    assert todo_object.priority == 0

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

def test_increase_priority(todo_object):
    assert todo_object.priority == 0
    todo_object.increase_priority()
    assert todo_object.priority == 1
    
def test_decrease_priority(todo_object):
    assert todo_object.priority == 0
    todo_object.decrease_priority()
    assert todo_object.priority == -1