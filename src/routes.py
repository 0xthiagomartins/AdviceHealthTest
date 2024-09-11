from flask import Blueprint, request, jsonify, current_app
from src.db import controllers
from src.auth import token_required
import traceback

api = Blueprint("api", __name__)


@api.route("/persons", methods=["POST"])
@token_required
def create_person():
    try:
        data = request.json
        current_app.logger.info(f"Attempting to create person with data: {data}")
        person_id = controllers.person.create(data={"name": data["name"]})
        current_app.logger.info(f"Person created with ID: {person_id}")
        person = controllers.person.get(by="id", value=person_id)
        current_app.logger.info(f"Retrieved person: {person}")
        return jsonify({"id": person["id"], "name": person["name"]}), 201
    except Exception as e:
        current_app.logger.error(f"Error creating person: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500


@api.route("/persons/<int:person_id>/cars", methods=["POST"])
@token_required
def add_car(person_id):
    try:
        data = request.json
        current_app.logger.info(
            f"Attempting to add car for person {person_id} with data: {data}"
        )
        person = controllers.person.get(by="id", value=person_id)
        if not person:
            current_app.logger.info(f"Person not found with ID: {person_id}")
            return jsonify({"error": "Person not found"}), 404

        cars = controllers.car.list(filter={"owner_id": person_id}, mode="all")
        if len(cars) >= 3:
            current_app.logger.info(f"Car limit reached for person {person_id}")
            return jsonify({"error": "Person already has 3 cars"}), 400

        car_data = {
            "color": data["color"],
            "model": data["model"],
            "owner_id": person_id,
        }
        car_id = controllers.car.create(data=car_data)
        current_app.logger.info(f"Car created with ID: {car_id}")
        car = controllers.car.get(by="id", value=car_id)
        current_app.logger.info(f"Retrieved car: {car}")
        return (
            jsonify({"id": car["id"], "color": car["color"], "model": car["model"]}),
            201,
        )
    except Exception as e:
        current_app.logger.error(f"Error adding car: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500
