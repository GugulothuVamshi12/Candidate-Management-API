# Candidate Management API

A simple FastAPI-based backend service for managing recruitment candidates.

## Features

- Create new candidates with validation
- View all candidates
- Filter candidates by status
- Update candidate status
- Email validation
- Status validation (applied, interview, selected, rejected)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### 3. Access API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Candidate

**POST** `/candidates`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "skill": "Python",
  "status": "applied"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "skill": "Python",
  "status": "applied"
}
```

### 2. Get All Candidates

**GET** `/candidates`

Optional query parameter: `?status=interview`

**Response** (200 OK):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "skill": "Python",
    "status": "applied"
  }
]
```

### 3. Update Candidate Status

**PUT** `/candidates/{id}/status`

```json
{
  "status": "interview"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "skill": "Python",
  "status": "interview"
}
```

## Validation Rules

- **Email**: Must be a valid email format
- **Status**: Must be one of: `applied`, `interview`, `selected`, `rejected`
- **Name**: Cannot be empty
- **Skill**: Cannot be empty
- **Duplicate Email**: Returns 400 error if email already exists

## Testing with cURL

### Create a candidate:
```bash
curl -X POST "http://localhost:8000/candidates" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "skill": "Python",
    "status": "applied"
  }'
```

### Get all candidates:
```bash
curl "http://localhost:8000/candidates"
```

### Filter by status:
```bash
curl "http://localhost:8000/candidates?status=interview"
```

### Update status:
```bash
curl -X PUT "http://localhost:8000/candidates/{id}/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "interview"}'
```

## Project Structure

```
.
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application