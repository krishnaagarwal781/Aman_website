from fastapi import FastAPI, HTTPException
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# Define Pydantic models for request and response

# Initialize FastAPI app
app = FastAPI()

# Testimonial endpoints
@app.get("/all-testimonial", response_model=list[Testimonial])
async def get_all_testimonials():
    coll = db["testimonials"]
    testimonials = list(coll.find({}, {"_id": 0}))
    return testimonials

@app.post("/create-testimonial", response_model=Testimonial)
async def create_testimonial(testimonial: Testimonial):
    coll = db["testimonials"]
    result = coll.insert_one(testimonial.dict())
    created_testimonial = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_testimonial

@app.patch("/edit-testimonial/{testimonial_id}", response_model=Testimonial)
async def edit_testimonial(testimonial_id: str, testimonial_data: Testimonial):
    coll = db["testimonials"]
    coll.update_one({"_id": ObjectId(testimonial_id)}, {"$set": testimonial_data.dict()})
    updated_testimonial = coll.find_one({"_id": ObjectId(testimonial_id)}, {"_id": 0})
    if updated_testimonial:
        return updated_testimonial
    else:
        raise HTTPException(status_code=404, detail="Testimonial not found")

@app.post("/delete-testimonial/{testimonial_id}")
async def delete_testimonial(testimonial_id: str):
    coll = db["testimonials"]
    result = coll.delete_one({"_id": ObjectId(testimonial_id)})
    if result.deleted_count == 1:
        return {"message": "Testimonial deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Testimonial not found")
