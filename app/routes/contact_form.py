from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *
from app.schemas.contact_schema import *

# Define Pydantic models for request and response


# Initialize FastAPI app
contactRouter = APIRouter()

# Contact Form endpoints
@contactRouter.post("/contact/submit-contact-form", tags=['Contact Form Routes'])
async def submit_contact_form(contact_form: ContactForm):
    result = contact_forms_collection.insert_one(contact_form.model_dump())
    return {"contact_form_id": str(result.inserted_id)}

@contactRouter.get("/contact/get-all-contact-form", tags=['Contact Form Routes'])
async def get_all_contact_forms():
    contact_forms = contact_forms_collection.find()
    return list_serial(contact_forms)

@contactRouter.patch("/contact/edit-contact-form/{contact_id}", tags=['Contact Form Routes'])
async def edit_contact_form(contact_id: str, contact_data: ContactForm):
    contact_forms_collection.update_one({"_id": ObjectId(contact_id)}, {"$set": contact_data.model_dump()})
    updated_contact_form = contact_forms_collection.find_one({"_id": ObjectId(contact_id)}, {"_id": 0})
    if updated_contact_form:
        return updated_contact_form
    else:
        raise HTTPException(status_code=404, detail="Contact form not found")