from flask import Blueprint, request, jsonify
from src.db import controllers
from src.auth import token_required

api = Blueprint("api", __name__)


@api.route("/persons", methods=["POST"])
@token_required
def create_person():
    data = request.json
    person_id = controllers.person.create(data={"name": data["name"]})
    person = controllers.person.get(by="id", value=person_id)
    return jsonify({"id": person["id"], "name": person["name"]}), 201


@api.route("/persons/<int:person_id>/cars", methods=["POST"])
@token_required
def add_car(person_id):
    data = request.json
    person = controllers.person.get(by="id", value=person_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404

    cars = controllers.car.list(filter={"owner_id": person_id}, mode="all")
    if len(cars) >= 3:
        return jsonify({"error": "Person already has 3 cars"}), 400

    car_data = {"color": data["color"], "model": data["model"], "owner_id": person_id}
    car_id = controllers.car.create(data=car_data)
    car = controllers.car.get(by="id", value=car_id)
    return jsonify({"id": car["id"], "color": car["color"], "model": car["model"]}), 201


# Add more routes as needed
