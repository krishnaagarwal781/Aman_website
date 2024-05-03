from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *

# Define Pydantic models for request and response


# Initialize FastAPI app
contactRouter = APIRouter()

# Contact Form endpoints
@contactRouter.post("/contact/submit-contact-form", response_model=ContactForm, tags=['Contact Form Routes'])
async def submit_contact_form(contact_form: ContactForm):
    coll = db["contact_forms"]
    result = coll.insert_one(contact_form.dict())
    created_contact_form = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_contact_form

@contactRouter.get("/contact/get-all-contact-form", response_model=list[ContactForm], tags=['Contact Form Routes'])
async def get_all_contact_forms():
    coll = db["contact_forms"]
    contact_forms = list(coll.find({}, {"_id": 0}))
    return contact_forms

@contactRouter.patch("/contact/edit-contact-form/{contact_id}", response_model=ContactForm, tags=['Contact Form Routes'])
async def edit_contact_form(contact_id: str, contact_data: ContactForm):
    coll = db["contact_forms"]
    coll.update_one({"_id": ObjectId(contact_id)}, {"$set": contact_data.dict()})
    updated_contact_form = coll.find_one({"_id": ObjectId(contact_id)}, {"_id": 0})
    if updated_contact_form:
        return updated_contact_form
    else:
        raise HTTPException(status_code=404, detail="Contact form not found")
