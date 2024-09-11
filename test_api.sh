#!/bin/bash

# Set the base URL for the API
BASE_URL="http://localhost:5001"  # Change this if you modified the port

# Health check
echo "Performing health check..."
HEALTH_RESPONSE=$(curl -s "${BASE_URL}/health")
echo "Health check response: $HEALTH_RESPONSE"

if [ "$HEALTH_RESPONSE" != "OK" ]; then
    echo "Health check failed. Make sure the API is running."
    exit 1
fi

# Generate a token
echo "Generating token..."
TOKEN_RESPONSE=$(curl -s "${BASE_URL}/generate_token")
TOKEN=$(echo $TOKEN_RESPONSE | grep -o '"token":"[^"]*' | grep -o '[^"]*$')

if [ -z "$TOKEN" ]; then
    echo "Failed to generate token"
    exit 1
fi

echo "Token generated successfully"

# Test creating a person
echo "Testing Create Person API..."
PERSON_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"name": "John Doe"}' \
    "${BASE_URL}/persons")

echo "Response: $PERSON_RESPONSE"

# Extract the person ID from the response (assuming the response is in JSON format)
PERSON_ID=$(echo $PERSON_RESPONSE | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ -z "$PERSON_ID" ]; then
    echo "Failed to create person or extract person ID"
    exit 1
fi

echo "Created person with ID: $PERSON_ID"

# Test adding a car to the person
echo "Testing Add Car API..."
CAR_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"color": "blue", "model": "sedan"}' \
    "${BASE_URL}/persons/${PERSON_ID}/cars")

echo "Response: $CAR_RESPONSE"

# Check if the car was added successfully
if [[ $CAR_RESPONSE == *"id"* ]]; then
    echo "Car added successfully"
else
    echo "Failed to add car"
fi

# Test adding more cars to reach and exceed the limit
for i in {2..4}
do
    echo "Adding car $i..."
    CAR_RESPONSE=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"color": "red", "model": "hatch"}' \
        "${BASE_URL}/persons/${PERSON_ID}/cars")

    echo "Response: $CAR_RESPONSE"

    if [[ $CAR_RESPONSE == *"error"* ]]; then
        echo "Reached car limit as expected"
        break
    fi
done

echo "API testing completed"