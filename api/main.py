from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from api.db import insert_complaint, get_complaint_by_id, get_complaint_by_mobile

app = FastAPI()

class RegisterRequest(BaseModel):
    name: str = Field(..., pattern=r"^[A-Za-z ]+$", description="Name should contain only letters and spaces.")
    mobile: str = Field(..., pattern=r"^\d{10}$", description="Enter a valid 10-digit mobile number.")
    complaint: str = Field(..., min_length=10, description="Complaint must be at least 10 characters.")

class StatusResponse(BaseModel):
    complaint_id: str
    name: str
    mobile: str
    complaint: str
    status: str

@app.post("/register")
async def register_complaint(request: RegisterRequest):
    try:
        # Generate unique complaint ID
        complaint_id = f"CMP{abs(hash(request.mobile + request.complaint)) % 10000:04}"

        result = {
            "complaint_id": complaint_id,
            "name": request.name.strip().title(),
            "mobile": request.mobile.strip(),
            "complaint": request.complaint.strip(),
            "status": "Registered"
        }

        insert_complaint(result)
        return {"complaint_id": complaint_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Failed to register complaint: {str(e)}")

@app.get("/status/{query}", response_model=StatusResponse)
async def get_status(query: str):
    query = query.strip()

    result = None
    if query.upper().startswith("CMP"):
        result = get_complaint_by_id(query.upper())
    elif query.isdigit() and len(query) == 10:
        result = get_complaint_by_mobile(query)
    else:
        raise HTTPException(
            status_code=400,
            detail="❌ Invalid input. Please provide a valid 10-digit mobile number or Complaint ID (e.g., CMP1234)."
        )

    if result:
        return result

    raise HTTPException(status_code=404, detail="❌ Complaint not found. Please verify the ID or mobile number.")
