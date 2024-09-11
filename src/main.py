from flask import Flask, jsonify
from src.routes import api
from src.auth import generate_token
from src.db.database import init_db
import os
import logging

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback_secret_key")
app.register_blueprint(api)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# Flag to track if the database has been initialized
db_initialized = False


@app.route("/health", methods=["GET"])
def health_check():
    app.logger.info("Health check endpoint called")
    return "OK", 200


@app.route("/generate_token", methods=["GET"])
def get_token():
    try:
        token = generate_token("test_user")
        return jsonify({"token": token}), 200
    except Exception as e:
        app.logger.error(f"Error generating token: {str(e)}")
        return jsonify({"error": "Failed to generate token"}), 500


@app.before_request
def initialize_database():
    global db_initialized
    if not db_initialized:
        init_db()
        app.logger.info("Database initialized")
        db_initialized = True


if __name__ == "__main__":
    app.logger.info("Starting the application")
    app.run(host="0.0.0.0", port=5000, debug=True)
