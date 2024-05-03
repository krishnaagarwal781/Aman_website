from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *

# Define Pydantic models for request and response


# Initialize FastAPI app
categoryRouter = APIRouter()

# Category endpoints
@categoryRouter.get("/category/all-category", response_model=list[Category], tags=['Category Routes'])
async def get_all_categories():
    categories = list(categories_collection.find({}, {"_id": 0}))
    return categories

@categoryRouter.post("/category/add-category", response_model=Category, tags=['Category Routes'])
async def add_category(category: Category):
    result = categories_collection.insert_one(category.dict())
    created_category = categories_collection.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_category

@categoryRouter.patch("/category/edit-category/{category_id}", response_model=Category, tags=['Category Routes'])
async def edit_category(category_id: str, category_data: Category):
    categories_collection.update_one({"_id": ObjectId(category_id)}, {"$set": category_data.dict()})
    updated_category = categories_collection.find_one({"_id": ObjectId(category_id)}, {"_id": 0})
    if updated_category:
        return updated_category
    else:
        raise HTTPException(status_code=404, detail="Category not found")

@categoryRouter.delete("/category/delete-category/{category_id}", tags=['Category Routes'])
async def delete_category(category_id: str):
    result = categories_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 1:
        return {"message": "Category deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Category not found")
