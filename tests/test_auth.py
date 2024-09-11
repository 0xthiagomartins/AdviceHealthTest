import pytest
from src.auth import token_required, generate_token
from flask import Flask, jsonify
import jwt
import os


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test_secret_key"

    @app.route("/protected")
    @token_required
    def protected():
        return jsonify({"message": "Access granted"})

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_missing_token(client):
    response = client.get("/protected")
    assert response.status_code == 401
    assert b"Token is missing!" in response.data


def test_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert b"Token is invalid!" in response.data


def test_valid_token(client, app):
    with app.app_context():
        token = generate_token("test_user")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert b"Access granted" in response.data
