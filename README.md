# Carford Car Shop Management System

This project is a Flask-based API for managing car owners and their vehicles for Carford car shop in Nork-Town. It allows adding car owners, registering cars to owners, and enforces the town's vehicle ownership limits.

## Features

- Add car owners
- Register cars to owners (up to 3 cars per person)
- Secure routes with JWT authentication
- SQLite database for data storage
- Docker support for easy deployment and testing

## Requirements

- Docker and Docker Compose
- Python 3.12 (if running locally without Docker)
- jq (for running integration tests)

## Getting Started

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/your-username/carford-car-shop.git
   cd carford-car-shop
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file and set your `SECRET_KEY`.

4. Run the application:
   ```
   python run.py
   ```

5. Run unit tests:
   ```
   pytest
   ```

### Development with Docker

1. Build and start the containers:
   ```
   docker-compose up --build
   ```

2. Run tests:
   ```
   docker-compose run test pytest
   ```

3. To stop the containers:
   ```
   docker-compose down
   ```

### Running Integration Tests

To run the integration tests, follow these steps:

1. Make sure the application is running (either locally or in Docker).

2. Install jq if you haven't already:
   ```
   sudo apt-get install jq  # For Ubuntu/Debian
   # or
   brew install jq  # For macOS with Homebrew
   ```

3. Run the integration test script:
   ```
   ./test_api.sh
   ```

This script will test the API endpoints, including health check, token generation, creating a person, and adding cars to a person.

## API Endpoints

- `POST /persons`: Create a new person
- `POST /persons/<person_id>/cars`: Add a car to a person

For detailed API documentation, refer to the API specification document (not included in this README).

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.