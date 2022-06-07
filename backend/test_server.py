from server import app
import json
import pytest
from middleware import repo_for_todo, repo_for_user

app.testing = True
client = app.test_client()


def test_user_signup(client=client):
    payload = json.dumps(
        {
            "name": "user_for_testing",
            "email": "user_for_testing@lums.edu.pk",
            "password": "random_string",
        }
    )
    res = client.post(
        "/signup", headers={"Content-Type": "application/json"}, data=payload
    )
    json_data = json.loads(res.data)
    assert json_data["success"] == True


@pytest.fixture(scope="function")
def valid_user_token(client=client):
    payload = json.dumps(
        {"email": "user_for_testing@lums.edu.pk", "password": "random_string"}
    )

    res = client.post(
        "/login", headers={"Content-Type": "application/json"}, data=payload
    )
    json_data = json.loads(res.data)
    assert json_data["success"] == True
    return json_data["token"]


def test_home_page(client=client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.data == b"<h1>Flask server by Tajir<h1>"


def test_login_user(client=client):
    payload = json.dumps(
        {"email": "user_for_testing@lums.edu.pk", "password": "random_string"}
    )
    res = client.post(
        "/login", headers={"Content-Type": "application/json"}, data=payload
    )
    assert res.status_code == 200
    json_data = json.loads(res.data)
    assert json_data["success"] == True
    assert json_data["token"] != None


def _create_todo(valid_user_token, client=client):
    payload = json.dumps(
        {"title": "test title", "description": "test description", "status": "OPEN"}
    )
    response = client.post(
        "/todos",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": valid_user_token},
    )
    return response


def _delete_todo(valid_user_token, client, uuid):
    response = client.delete(
        "/todo/{}".format(uuid),
        headers={"Content-Type": "application/json", "Authorization": valid_user_token},
    )
    return response


def test_delete_todo(valid_user_token, client=client):
    created_todo = _create_todo(valid_user_token, client)
    response = json.loads(created_todo.data)
    assert response["success"] == True
    res = _delete_todo(valid_user_token, client, response["todo_id"])
    res = json.loads(res.data)
    assert res["success"] == True


def test_create_todo(valid_user_token, client=client):
    response = _create_todo(valid_user_token, client)
    json_data = json.loads(response.data)
    assert json_data["success"] == True
    # db clean up
    repo = repo_for_todo()
    todo = repo.get_by_id(json_data["todo_id"])
    repo.delete(todo)


def test_increase_priority(valid_user_token, client=client):
    response1 = _create_todo(valid_user_token, client)

    json_data = json.loads(response1.data)
    uuid_of_todo1 = json_data["todo_id"]

    res = client.post(
        "/todo/{}/increase_priority".format(uuid_of_todo1),
        headers={
            "Authorization": valid_user_token,
            "Content-Type": "application/json",
        },
    )
    assert res.status_code == 200
    json_data = json.loads(res.data)
    assert json_data["success"] == True
    # db clean up
    repo = repo_for_todo()
    todo = repo.get_by_id(uuid_of_todo1)
    repo.delete(todo)


def test_update_status(valid_user_token, client=client):
    response = _create_todo(valid_user_token, client)

    json_data = json.loads(response.data)
    uuid_of_todo = json_data["todo_id"]

    repo = repo_for_todo()
    todo = repo.get_by_id(uuid_of_todo)
    assert todo.status == "OPEN"

    res = client.post(
        "/todo/{}/updateStatus/{}".format(uuid_of_todo, "CLOSED"),
        headers={"Content-Type": "application/json", "Authorization": valid_user_token},
    )

    assert res.status_code == 200
    json_data = json.loads(res.data)
    print(json_data)
    assert json_data["success"] == True

    repo = repo_for_todo()
    todo_ = repo.get_by_id(uuid_of_todo)
    assert todo_.status == "CLOSED"
