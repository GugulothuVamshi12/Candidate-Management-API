"""
Test script for Candidate Management API
Run this after starting the server with: python main.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(response, title):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_api():
    """Test all API endpoints"""
    
    print("\n Starting API Tests...")
    
    # Test 1: Create first candidate
    print("\n Test 1: Create Candidate - John Doe")
    candidate1 = {
        "name": "John Doe",
        "email": "john@example.com",
        "skill": "Python",
        "status": "applied"
    }
    response = requests.post(f"{BASE_URL}/candidates", json=candidate1)
    print_response(response, "POST /candidates - Create John Doe")
    candidate1_id = response.json().get("id") if response.status_code in [200, 201] else None
    
    # Test 2: Create second candidate
    print("\n Test 2: Create Candidate - Jane Smith")
    candidate2 = {
        "name": "Jane Smith",
        "email": "jane@example.com",
        "skill": "JavaScript",
        "status": "interview"
    }
    response = requests.post(f"{BASE_URL}/candidates", json=candidate2)
    print_response(response, "POST /candidates - Create Jane Smith")
    candidate2_id = response.json().get("id") if response.status_code in [200, 201] else None
    
    # Test 3: Create third candidate
    print("\n Test 3: Create Candidate - Bob Wilson")
    candidate3 = {
        "name": "Bob Wilson",
        "email": "bob@example.com",
        "skill": "Java",
        "status": "selected"
    }
    response = requests.post(f"{BASE_URL}/candidates", json=candidate3)
    print_response(response, "POST /candidates - Create Bob Wilson")
    
    # Test 4: Try to create duplicate email (should fail)
    print("\n Test 4: Create Duplicate Email (Should Fail)")
    duplicate = {
        "name": "John Duplicate",
        "email": "john@example.com",
        "skill": "Python",
        "status": "applied"
    }
    response = requests.post(f"{BASE_URL}/candidates", json=duplicate)
    print_response(response, "POST /candidates - Duplicate Email")
    
    # Test 5: Get all candidates
    print("\n Test 5: Get All Candidates")
    response = requests.get(f"{BASE_URL}/candidates")
    print_response(response, "GET /candidates - All Candidates")
    
    # Test 6: Filter by status - interview
    print("\n Test 6: Filter Candidates by Status - interview")
    response = requests.get(f"{BASE_URL}/candidates?status=interview")
    print_response(response, "GET /candidates?status=interview")
    
    # Test 7: Filter by status - selected
    print("\n Test 7: Filter Candidates by Status - selected")
    response = requests.get(f"{BASE_URL}/candidates?status=selected")
    print_response(response, "GET /candidates?status=selected")
    
    # Test 8: Update candidate status
    if candidate1_id:
        print(f"\n Test 8: Update Candidate Status - {candidate1_id}")
        status_update = {"status": "interview"}
        response = requests.put(f"{BASE_URL}/candidates/{candidate1_id}/status", json=status_update)
        print_response(response, f"PUT /candidates/{candidate1_id}/status")
    
    # Test 9: Update to another status
    if candidate2_id:
        print(f"\n Test 9: Update Candidate Status - {candidate2_id}")
        status_update = {"status": "selected"}
        response = requests.put(f"{BASE_URL}/candidates/{candidate2_id}/status", json=status_update)
        print_response(response, f"PUT /candidates/{candidate2_id}/status")
    
    # Test 10: Try to update non-existent candidate (should fail)
    print("\n Test 10: Update Non-existent Candidate (Should Fail)")
    status_update = {"status": "rejected"}
    response = requests.put(f"{BASE_URL}/candidates/invalid-id/status", json=status_update)
    print_response(response, "PUT /candidates/invalid-id/status")
    
    # Test 11: Invalid email validation
    print("\n Test 11: Invalid Email (Should Fail)")
    invalid_candidate = {
        "name": "Invalid User",
        "email": "not-an-email",
        "skill": "Testing",
        "status": "applied"
    }
    response = requests.post(f"{BASE_URL}/candidates", json=invalid_candidate)
    print_response(response, "POST /candidates - Invalid Email")
    
    # Test 12: Invalid status
    print("\n Test 12: Invalid Status (Should Fail)")
    invalid_status = {
        "name": "Test User",
        "email": "test@example.com",
        "skill": "Testing",
        "status": "invalid_status"
    }
    response = requests.post(f"{BASE_URL}/candidates", json=invalid_status)
    print_response(response, "POST /candidates - Invalid Status")
    
    # Final: Get all candidates after updates
    print("\n Final: Get All Candidates After Updates")
    response = requests.get(f"{BASE_URL}/candidates")
    print_response(response, "GET /candidates - Final State")
    
    print("\n All tests completed!")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        # Check if server is running
        response = requests.get(BASE_URL)
        print(" Server is running!")
        test_api()
    except requests.exceptions.ConnectionError:
        print(" Error: Server is not running!")
        print("Please start the server first with: python main.py")
        print("Or: uvicorn main:app --reload")
