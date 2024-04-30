from fastapi import FastAPI, HTTPException
from bson import ObjectId

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]

# Define Pydantic models for request and response


# Initialize FastAPI app
app = FastAPI()

# Category endpoints
@app.get("/all-category", response_model=list[Category])
async def get_all_categories():
    coll = db["categories"]
    categories = list(coll.find({}, {"_id": 0}))
    return categories

@app.post("/add-category", response_model=Category)
async def add_category(category: Category):
    coll = db["categories"]
    result = coll.insert_one(category.dict())
    created_category = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_category

@app.patch("/edit-category/{category_id}", response_model=Category)
async def edit_category(category_id: str, category_data: Category):
    coll = db["categories"]
    coll.update_one({"_id": ObjectId(category_id)}, {"$set": category_data.dict()})
    updated_category = coll.find_one({"_id": ObjectId(category_id)}, {"_id": 0})
    if updated_category:
        return updated_category
    else:
        raise HTTPException(status_code=404, detail="Category not found")

@app.delete("/delete-category/{category_id}")
async def delete_category(category_id: str):
    coll = db["categories"]
    result = coll.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"message": "Category deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Category not found")
