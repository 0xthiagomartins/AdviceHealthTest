#!/bin/bash

BASE_URL="http://localhost:5000"  

# Health check
echo "Performing health check..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${BASE_URL}/health")
HTTP_STATUS=$(echo "$HEALTH_RESPONSE" | tail -n1)
HEALTH_BODY=$(echo "$HEALTH_RESPONSE" | sed '$d')

echo "Health check response (Status: $HTTP_STATUS): $HEALTH_BODY"

if [ "$HTTP_STATUS" != "200" ] || [ "$HEALTH_BODY" != "OK" ]; then
    echo "Health check failed. Make sure the API is running."
    exit 1
fi

# Generate a token
echo "Generating token..."
TOKEN_RESPONSE=$(curl -s -w "\n%{http_code}" "${BASE_URL}/generate_token")
TOKEN_STATUS=$(echo "$TOKEN_RESPONSE" | tail -n1)
TOKEN_BODY=$(echo "$TOKEN_RESPONSE" | sed '$d')

echo "Token generation response (Status: $TOKEN_STATUS): $TOKEN_BODY"

if [ "$TOKEN_STATUS" != "200" ]; then
    echo "Failed to generate token: Non-200 status code"
    exit 1
fi

# Extract token using awk
TOKEN=$(echo "$TOKEN_BODY" | awk -F'"' '/"token":/{print $4}')

if [ -z "$TOKEN" ]; then
    echo "Failed to extract token from response"
    exit 1
fi

echo "Token generated successfully: $TOKEN"

# Test creating a person
echo "Testing Create Person API..."
PERSON_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"name": "John Doe"}' \
    "${BASE_URL}/persons")

echo "Response: $PERSON_RESPONSE"

# Extract the person ID from the response using jq
if command -v jq &> /dev/null; then
    PERSON_ID=$(echo "$PERSON_RESPONSE" | jq -r '.id')
else
    echo "jq is not installed. Please install jq or use an alternative method to parse JSON."
    exit 1
fi

if [ -z "$PERSON_ID" ] || [ "$PERSON_ID" = "null" ]; then
    echo "Failed to create person or extract person ID"
    echo "Raw PERSON_RESPONSE:"
    echo "$PERSON_RESPONSE" | jq '.'
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
        -d '{"color": "YELLOW", "model": "HATCH"}' \
        "${BASE_URL}/persons/${PERSON_ID}/cars")

    echo "Response: $CAR_RESPONSE"

    if [[ $CAR_RESPONSE == *"error"* ]]; then
        echo "Reached car limit as expected"
        break
    fi
done

echo "API testing completed"