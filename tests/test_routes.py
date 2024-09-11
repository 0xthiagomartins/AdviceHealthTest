import pytest
from src.main import app
from src.db import controllers
from src.auth import generate_token
import json


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_headers():
    with app.app_context():
        token = generate_token("test_user")
    return {"Authorization": f"Bearer {token}"}


def test_create_person(client, mocker, auth_headers):
    mocker.patch.object(controllers.person, "create", return_value=1)
    mocker.patch.object(
        controllers.person, "get", return_value={"id": 1, "name": "John Doe"}
    )

    response = client.post("/persons", json={"name": "John Doe"}, headers=auth_headers)
    assert response.status_code == 201
    assert json.loads(response.data) == {"id": 1, "name": "John Doe"}


def test_add_car(client, mocker, auth_headers):
    mocker.patch.object(
        controllers.person, "get", return_value={"id": 1, "name": "John Doe"}
    )
    mocker.patch.object(controllers.car, "list", return_value=[])
    mocker.patch.object(controllers.car, "create", return_value=1)
    mocker.patch.object(
        controllers.car,
        "get",
        return_value={"id": 1, "color": "blue", "model": "sedan"},
    )

    response = client.post(
        "/persons/1/cars",
        json={"color": "blue", "model": "sedan"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert json.loads(response.data) == {"id": 1, "color": "blue", "model": "sedan"}


def test_add_car_person_not_found(client, mocker, auth_headers):
    mocker.patch.object(controllers.person, "get", return_value=None)

    response = client.post(
        "/persons/1/cars",
        json={"color": "blue", "model": "sedan"},
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert json.loads(response.data) == {"error": "Person not found"}


def test_add_car_limit_reached(client, mocker, auth_headers):
    mocker.patch.object(
        controllers.person, "get", return_value={"id": 1, "name": "John Doe"}
    )
    mocker.patch.object(controllers.car, "list", return_value=[{}, {}, {}])

    response = client.post(
        "/persons/1/cars",
        json={"color": "blue", "model": "sedan"},
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert json.loads(response.data) == {"error": "Person already has 3 cars"}
