from src.main import app

if __name__ == "__main__":
    app.logger.info("Starting the application")
    app.run(host="0.0.0.0", port=5000)
