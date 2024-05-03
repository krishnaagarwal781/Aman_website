from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *

# Define Pydantic models for request and response

# Initialize FastAPI app
testimonyRouter = APIRouter()

# Testimonial endpoints
@testimonyRouter.get("/testimony/all-testimonial", response_model=list[Testimonial], tags=['Testimony Routes'])
async def get_all_testimonials():
    coll = db["testimonials"]
    testimonials = list(coll.find({}, {"_id": 0}))
    return testimonials

@testimonyRouter.post("/testimony/create-testimonial", response_model=Testimonial, tags=['Testimony Routes'])
async def create_testimonial(testimonial: Testimonial):
    coll = db["testimonials"]
    result = coll.insert_one(testimonial.dict())
    created_testimonial = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_testimonial

@testimonyRouter.patch("/testimony/edit-testimonial/{testimonial_id}", response_model=Testimonial, tags=['Testimony Routes'])
async def edit_testimonial(testimonial_id: str, testimonial_data: Testimonial):
    coll = db["testimonials"]
    coll.update_one({"_id": ObjectId(testimonial_id)}, {"$set": testimonial_data.dict()})
    updated_testimonial = coll.find_one({"_id": ObjectId(testimonial_id)}, {"_id": 0})
    if updated_testimonial:
        return updated_testimonial
    else:
        raise HTTPException(status_code=404, detail="Testimonial not found")

@testimonyRouter.post("/testimony/delete-testimonial/{testimonial_id}", tags=['Testimony Routes'])
async def delete_testimonial(testimonial_id: str):
    coll = db["testimonials"]
    result = coll.delete_one({"_id": ObjectId(testimonial_id)})
    if result.deleted_count == 1:
        return {"message": "Testimonial deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Testimonial not found")
