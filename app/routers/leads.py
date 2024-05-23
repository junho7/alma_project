from fastapi import APIRouter, Form, Path, Depends, status
from fastapi.exceptions import HTTPException
from app.utils.auth import get_current_user
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from app.utils.email_utils import send_confirmation_email
from app.models.database import leads_collection

router = APIRouter()

# Form Data Validation
class LeadForm(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    resume: str = Field(..., max_length=1000)


# API Endpoint to Handle Form Submission
@router.post("/submit_lead")
async def submit_lead(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    resume: str = Form(...),
):
    # Validate Form Data
    lead_data = LeadForm(
        first_name=first_name, last_name=last_name, email=email, resume=resume
    )

    # Store Data in MongoDB
    document = {
        "first_name": lead_data.first_name,
        "last_name": lead_data.last_name,
        "email": lead_data.email,
        "resume": lead_data.resume,
        "state": "PENDING",
    }
    await leads_collection.insert_one(document)

    # Send Confirmation Email
    send_confirmation_email(lead_data)

    return {"message": "Resume submitted successfully"}


@router.get("/get_leads", dependencies=[Depends(get_current_user)])
async def get_all_leads():
    leads = []
    async for lead in leads_collection.find():
        lead["_id"] = str(lead["_id"])
        leads.append(lead)
    return {"leads": leads}
  
@router.put("/reach_out/{lead_id}", dependencies=[Depends(get_current_user)])
async def reach_out_to_lead(
    lead_id: str = Path(...),
):
    result = await leads_collection.update_one(
        {"_id": ObjectId(lead_id), "state": "PENDING"},
        {"$set": {"state": "REACHED_OUT"}},
    )

    if result.modified_count == 1:
        return {"message": f"Lead {lead_id} marked as REACHED_OUT"}
    else:
        raise HTTPException(
            status_code=404, detail="Lead not found or already REACHED_OUT"
        )