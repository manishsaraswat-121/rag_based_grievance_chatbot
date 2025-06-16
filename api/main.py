from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import re
import random

from api.db import insert_complaint, get_complaint_by_id

app = FastAPI(title="Grievance Complaint API")


class ComplaintCreate(BaseModel):
    name: str = Field(..., min_length=2)
    phone_number: str = Field(..., pattern=r"^\d{10}$", description="Enter a valid 10-digit phone number.")
    email: EmailStr
    complaint_details: str = Field(..., min_length=10)


class ComplaintResponse(BaseModel):
    complaint_id: str
    name: str
    phone_number: str
    email: str
    complaint_details: str
    created_at: str


def generate_complaint_id() -> str:
    """Generates a complaint ID like CMP1234"""
    return f"CMP{random.randint(1000, 9999)}"


@app.post("/complaints", response_model=dict)
def create_complaint(data: ComplaintCreate):
    created_at = datetime.now().isoformat()

    # Try up to 5 times to generate a unique complaint ID
    for _ in range(5):
        complaint_id = generate_complaint_id()

        complaint_data = {
            "complaint_id": complaint_id,
            "name": data.name.strip().title(),
            "phone_number": data.phone_number.strip(),
            "email": data.email.strip().lower(),
            "complaint_details": data.complaint_details.strip(),
            "created_at": created_at
        }

        try:
            inserted_id = insert_complaint(complaint_data)
            if inserted_id != complaint_id:
                return {
                    "complaint_id": inserted_id,
                    "message": f"⚠️ Complaint already exists. Reusing Complaint ID: {inserted_id}"
                }

            return {
                "complaint_id": inserted_id,
                "message": "✅ Complaint created successfully"
            }
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                continue
            raise HTTPException(status_code=500, detail=f"❌ Failed to register complaint: {str(e)}")

    raise HTTPException(status_code=500, detail="❌ Failed to generate unique complaint ID. Please try again.")


@app.get("/complaints/{complaint_id}", response_class=PlainTextResponse)
def get_complaint(complaint_id: str):
    complaint_id = complaint_id.strip().upper()

    if not re.fullmatch(r"CMP\d{4}", complaint_id):
        raise HTTPException(
            status_code=400,
            detail="❌ Invalid Complaint ID format. Use format like CMP1234."
        )

    result = get_complaint_by_id(complaint_id)
    if not result:
        raise HTTPException(status_code=404, detail="❌ Complaint not found.")

    # Return plain text response with line breaks
    return (
        f"Complaint Details:\n"
        f"• Complaint ID: {result['complaint_id']}\n"
        f"• Name: {result['name']}\n"
        f"• Phone: {result['phone_number']}\n"
        f"• Email: {result['email']}\n"
        f"• Complaint: {result['complaint_details']}\n"
        f"• Created At: {result['created_at']}"
    )
