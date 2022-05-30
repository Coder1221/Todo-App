from server import app
import json
import pytest

app.testing = True
client = app.test_client()


@pytest.fixture(scope="function")
def test_valid_user_token(client=client):
    payload = json.dumps(
        {"email": "user_for_testing@lums.edu.pk", "password": "random_string"}
    )

    res = client.get(
        "/login", headers={"Content-Type": "application/json"}, data=payload
    )
    json_data = json.loads(res.data)
    assert json_data["success"] == True
    return json_data["token"]
