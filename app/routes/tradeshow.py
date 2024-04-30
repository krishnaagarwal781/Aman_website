from fastapi import FastAPI, HTTPException
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# Define Pydantic models for request and response


# Initialize FastAPI app
app = FastAPI()

# Tradeshow endpoints
@app.get("/all-tradeshow", response_model=list[Tradeshow])
async def get_all_tradeshows():
    coll = db["tradeshows"]
    tradeshows = list(coll.find({}, {"_id": 0}))
    return tradeshows

@app.post("/create-tradeshow", response_model=Tradeshow)
async def create_tradeshow(tradeshow: Tradeshow):
    coll = db["tradeshows"]
    result = coll.insert_one(tradeshow.dict())
    created_tradeshow = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_tradeshow

@app.patch("/edit-tradeshow/{tradeshow_id}", response_model=Tradeshow)
async def edit_tradeshow(tradeshow_id: str, tradeshow_data: Tradeshow):
    coll = db["tradeshows"]
    coll.update_one({"_id": ObjectId(tradeshow_id)}, {"$set": tradeshow_data.dict()})
    updated_tradeshow = coll.find_one({"_id": ObjectId(tradeshow_id)}, {"_id": 0})
    if updated_tradeshow:
        return updated_tradeshow
    else:
        raise HTTPException(status_code=404, detail="Tradeshow not found")

@app.post("/delete-tradeshow/{tradeshow_id}")
async def delete_tradeshow(tradeshow_id: str):
    coll = db["tradeshows"]
    result = coll.delete_one({"_id": ObjectId(tradeshow_id)})
    if result.deleted_count == 1:
        return {"message": "Tradeshow deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Tradeshow not found")
