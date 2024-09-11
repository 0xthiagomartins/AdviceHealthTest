from flask import Flask, jsonify
from src.routes import api
from src.auth import generate_token
import os
import logging

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback_secret_key")
app.register_blueprint(api)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)


@app.route("/health", methods=["GET"])
def health_check():
    app.logger.info("Health check endpoint called")
    return "OK", 200


@app.route("/generate_token", methods=["GET"])
def get_token():
    token = generate_token("test_user")
    return jsonify({"token": token})


if __name__ == "__main__":
    app.logger.info("Starting the application")
    app.run(host="0.0.0.0", port=5000, debug=True)
