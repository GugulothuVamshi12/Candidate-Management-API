#!/bin/bash

# Candidate Management API Demo Script
# This script demonstrates all API endpoints using curl

echo "Candidate Management API Demo"
echo "=================================="
echo ""

BASE_URL="http://localhost:8000"

# Check if server is running
echo "Checking if server is running..."
if ! curl -s "$BASE_URL" > /dev/null; then
    echo "Server is not running!"
    echo "Please start the server first with: python main.py"
    exit 1
fi
echo "Server is running!"
echo ""

# Test 1: Create first candidate
echo "Test 1: Creating candidate - John Doe"
echo "----------------------------------------"
curl -X POST "$BASE_URL/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "skill": "Python",
    "status": "applied"
  }' | jq '.'
echo ""
echo ""

# Test 2: Create second candidate
echo "Test 2: Creating candidate - Jane Smith"
echo "-------------------------------------------"
JANE_RESPONSE=$(curl -s -X POST "$BASE_URL/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "skill": "JavaScript",
    "status": "interview"
  }')
echo "$JANE_RESPONSE" | jq '.'
JANE_ID=$(echo "$JANE_RESPONSE" | jq -r '.id')
echo ""
echo ""

# Test 3: Get all candidates
echo "Test 3: Getting all candidates"
echo "----------------------------------"
curl -s "$BASE_URL/candidates" | jq '.'
echo ""
echo ""

# Test 4: Filter by status
echo "Test 4: Filtering candidates by status=interview"
echo "----------------------------------------------------"
curl -s "$BASE_URL/candidates?status=interview" | jq '.'
echo ""
echo ""

# Test 5: Update candidate status
if [ ! -z "$JANE_ID" ]; then
    echo "Test 5: Updating Jane's status to 'selected'"
    echo "-----------------------------------------------"
    curl -s -X PUT "$BASE_URL/candidates/$JANE_ID/status" \
      -H "Content-Type: application/json" \
      -d '{"status": "selected"}' | jq '.'
    echo ""
    echo ""
fi

# Test 6: Get all candidates after update
echo "Test 6: Getting all candidates after update"
echo "-----------------------------------------------"
curl -s "$BASE_URL/candidates" | jq '.'
echo ""
echo ""

# Test 7: Try invalid email (should fail)
echo "Test 7: Trying to create candidate with invalid email"
echo "---------------------------------------------------------"
curl -s -X POST "$BASE_URL/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid User",
    "email": "not-an-email",
    "skill": "Testing",
    "status": "applied"
  }' | jq '.'
echo ""
echo ""

# Test 8: Try duplicate email (should fail)
echo "Test 8: Trying to create duplicate email"
echo "-------------------------------------------"
curl -s -X POST "$BASE_URL/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Duplicate John",
    "email": "john@example.com",
    "skill": "Python",
    "status": "applied"
  }' | jq '.'
echo ""
echo ""

echo "Demo completed!"
echo ""
echo "Tip: Visit http://localhost:8000/docs for interactive API documentation"


