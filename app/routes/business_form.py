from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# Define Pydantic models for request and response


# Initialize FastAPI app
app = FastAPI()

# Business Form endpoints
@app.post("/submit-business-form", response_model=BusinessForm)
async def submit_business_form(business_form: BusinessForm):
    coll = db["business_forms"]
    result = coll.insert_one(business_form.dict())
    created_business_form = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_business_form

@app.get("/get-all-business-form", response_model=list[BusinessForm])
async def get_all_business_forms():
    coll = db["business_forms"]
    business_forms = list(coll.find({}, {"_id": 0}))
    return business_forms

@app.patch("/edit-business-form/{business_id}", response_model=BusinessForm)
async def edit_business_form(business_id: str, business_data: BusinessForm):
    coll = db["business_forms"]
    coll.update_one({"_id": ObjectId(business_id)}, {"$set": business_data.dict()})
    updated_business_form = coll.find_one({"_id": ObjectId(business_id)}, {"_id": 0})
    if updated_business_form:
        return updated_business_form
    else:
        raise HTTPException(status_code=404, detail="Business form not found")
