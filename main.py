from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Literal
from uuid import uuid4

app = FastAPI(title="Candidate Management API")

# In-memory storage for candidates
candidates_db = {}

# Pydantic models
class CandidateCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Candidate's full name")
    email: EmailStr = Field(..., description="Valid email address")
    skill: str = Field(..., min_length=1, description="Primary skill")
    status: Literal["applied", "interview", "selected", "rejected"] = Field(
        default="applied",
        description="Current status of the candidate"
    )
    
    @field_validator('status')
    @classmethod
    def validate_status(cls, v):
        valid_statuses = {"applied", "interview", "selected", "rejected"}
        if v not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return v

class CandidateResponse(CandidateCreate):
    id: str = Field(..., description="Unique candidate ID")

class StatusUpdate(BaseModel):
    status: Literal["applied", "interview", "selected", "rejected"] = Field(
        ...,
        description="New status for the candidate"
    )

# API Endpoints

@app.post("/candidates", response_model=CandidateResponse, status_code=201)
async def create_candidate(candidate: CandidateCreate):
    """
    Create a new candidate.
    
    - **name**: Candidate's full name (required)
    - **email**: Valid email address (required)
    - **skill**: Primary skill (required)
    - **status**: One of: applied, interview, selected, rejected (default: applied)
    """
    # Check if email already exists
    for existing_candidate in candidates_db.values():
        if existing_candidate.get("email") == candidate.email:
            raise HTTPException(
                status_code=400,
                detail=f"Candidate with email {candidate.email} already exists"
            )
    
    # Generate unique ID
    candidate_id = str(uuid4())
    
    # Store candidate
    candidate_data = candidate.model_dump()
    candidate_data["id"] = candidate_id
    candidates_db[candidate_id] = candidate_data
    
    return candidate_data

@app.get("/candidates", response_model=List[CandidateResponse])
async def get_candidates(
    status: Optional[Literal["applied", "interview", "selected", "rejected"]] = Query(
        None,
        description="Filter candidates by status"
    )
):
    """
    Get all candidates with optional status filtering.
    
    - **status** (optional): Filter by status (applied, interview, selected, rejected)
    """
    if status:
        # Filter by status
        filtered_candidates = [
            candidate for candidate in candidates_db.values()
            if candidate["status"] == status
        ]
        return filtered_candidates
    
    # Return all candidates
    return list(candidates_db.values())

@app.put("/candidates/{id}/status", response_model=CandidateResponse)
async def update_candidate_status(id: str, status_update: StatusUpdate):
    """
    Update the status of a candidate.
    
    - **id**: Candidate ID (path parameter)
    - **status**: New status (applied, interview, selected, rejected)
    """
    # Check if candidate exists
    if id not in candidates_db:
        raise HTTPException(
            status_code=404,
            detail=f"Candidate with id {id} not found"
        )
    
    # Update status
    candidates_db[id]["status"] = status_update.status
    
    return candidates_db[id]

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Candidate Management API",
        "endpoints": {
            "POST /candidates": "Create a new candidate",
            "GET /candidates": "Get all candidates (optional ?status= filter)",
            "PUT /candidates/{id}/status": "Update candidate status"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

