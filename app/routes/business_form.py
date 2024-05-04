from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from bson import ObjectId

from app.models.models import *
from app.config.private import *
from app.schemas.business_schema import *

businessRouter = APIRouter()

# Business Form endpoints
@businessRouter.post("/business/submit-business-form", tags=['Business Form Routes'])
async def submit_business_form(business_form: BusinessForm):
    result = business_forms_collection.insert_one(business_form.model_dump())
    # created_business_form = business_forms_collection.find_one({"_id": result.inserted_id}, {"_id": 0})
    return {"business_form_id": str(result.inserted_id)}

@businessRouter.get("/business/get-all-business-form", tags=['Business Form Routes'])
async def get_all_business_forms():
    business_forms = business_forms_collection.find()
    return list_serial(business_forms)

@businessRouter.get("/business/get-business-form", tags=['Business Form Routes'])
async def get_business_form(business_id: str):
    business_form = business_forms_collection.find_one({"_id": ObjectId(business_id)})
    return individual_serial(business_form)

@businessRouter.patch("/business/edit-business-form/{business_id}", tags=['Business Form Routes'])
async def edit_business_form(business_id: str, business_data: BusinessForm):
    business_forms_collection.update_one({"_id": ObjectId(business_id)}, {"$set": business_data.model_dump()})
    updated_business_form = business_forms_collection.find_one({"_id": ObjectId(business_id)}, {"_id": 0})
    if updated_business_form:
        return updated_business_form
    else:
        raise HTTPException(status_code=404, detail="Business form not found")
