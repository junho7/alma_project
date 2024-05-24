import base64
from bson import ObjectId
from fastapi import APIRouter, Depends, File, Form, Path, UploadFile
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, EmailStr
from app.models.database import leads_collection
from app.utils.auth import get_current_user
from app.utils.email_utils import send_confirmation_email

router = APIRouter()


# Form Data Validation
class LeadForm(BaseModel):
    first_name: str = Form(...)
    last_name: str = Form(...)
    email: EmailStr = Form(...)
    resume: UploadFile = File(...)


# API Endpoint to Handle Form Submission
@router.post("/submit_lead")
async def submit_lead(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: EmailStr = Form(...),
    resume: UploadFile = File(...)
    ):
    contents = await resume.read()
    filename = resume.filename

    # Store Data in MongoDB
    document = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "resume_filename": filename,
        "resume_contents": contents,
        "state": "PENDING",
    }
    await leads_collection.insert_one(document)

    # Send Confirmation Email
    send_confirmation_email(document)

    return {"message": "Resume submitted successfully"}


@router.get("/get_leads", dependencies=[Depends(get_current_user)])
async def get_all_leads():
    leads = []
    async for lead in leads_collection.find():
        lead["_id"] = str(lead["_id"])
        if "resume_contents" in lead:
            lead["resume_contents"] = base64.b64encode(lead["resume_contents"]).decode() # Encode as Base64
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
