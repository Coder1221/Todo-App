from pydoc import cram
from zipapp import create_archive
from todo import model as td
import json


def create_test_object():
    uuid = "2w1jdsj21@3"
    title = "my_title"
    description = "short description"
    status = 1
    created_data_class = td.Todo(uuid, title, description, status, None, None, None)
    return created_data_class


def test_todo_creation():
    created_data_class = create_test_object()
    assert created_data_class.uuid == "2w1jdsj21@3"
    assert created_data_class.title == "my_title"
    assert created_data_class.description == "short description"
    assert created_data_class.status == 1


def test_update_status():
    created_data_class = create_test_object()
    # status should be updated when provided string enum
    created_data_class.update_status("IN_PROGRESS")
    assert created_data_class.status == 2
    #  status should not be updated
    created_data_class.update_status("IN_validValue")
    assert created_data_class.status == 2
    # status shoud be updated by providing enum value
    created_data_class.update_status(3)
    assert created_data_class.status == 3
    # status should not be updated provided wrong enum value
    created_data_class.update_status(22)
    assert created_data_class.status != 22


def test_update_title():
    created_data_class = create_test_object()
    prev_title = created_data_class.title
    created_data_class.update_title("My new Title")
    assert created_data_class.title != prev_title
    assert created_data_class.title == "My new Title"


def test_update_description():
    created_data_class = create_test_object()
    prev_description = created_data_class.description
    created_data_class.update_description("My new Description")
    assert created_data_class.description != prev_description
    assert created_data_class.description == "My new Description"


def test_model_should_return_json():
    created_data_class = create_test_object()
    parsed_json = json.loads(created_data_class.to_json())
    assert isinstance(parsed_json, dict) == True
    assert parsed_json["title"] == "my_title"
