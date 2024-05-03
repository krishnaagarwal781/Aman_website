from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from bson import ObjectId

from app.models.models import *
from app.config.private import *

businessRouter = APIRouter()

# Business Form endpoints
@businessRouter.post("/business/submit-business-form", response_model=BusinessForm, tags=['Business Form Routes'])
async def submit_business_form(business_form: BusinessForm):
    result = business_forms_collection.insert_one(business_form.dict())
    created_business_form = business_forms_collection.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_business_form

@businessRouter.get("/business/get-all-business-form", response_model=list[BusinessForm], tags=['Business Form Routes'])
async def get_all_business_forms():
    business_forms = list(business_forms_collection.find({}, {"_id": 0}))
    return business_forms

@businessRouter.patch("/business/edit-business-form/{business_id}", response_model=BusinessForm, tags=['Business Form Routes'])
async def edit_business_form(business_id: str, business_data: BusinessForm):
    business_forms_collection.update_one({"_id": ObjectId(business_id)}, {"$set": business_data.dict()})
    updated_business_form = business_forms_collection.find_one({"_id": ObjectId(business_id)}, {"_id": 0})
    if updated_business_form:
        return updated_business_form
    else:
        raise HTTPException(status_code=404, detail="Business form not found")
