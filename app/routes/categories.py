from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *
from app.schemas.category_schema import *

categoryRouter = APIRouter()

# Category endpoints
@categoryRouter.get("/category/get-all-category", tags=['Category Routes'])
async def get_all_categories():
    categories = categories_collection.find()
    return list_serial(categories)

@categoryRouter.post("/category/add-category", tags=['Category Routes'])
async def add_category(category: Category):
    result = categories_collection.insert_one(category.model_dump())
    return {"category_id": str(result.inserted_id)}

@categoryRouter.patch("/category/edit-category/{category_id}", tags=['Category Routes'])
async def edit_category(category_id: str, category_data: Category):
    categories_collection.update_one({"_id": ObjectId(category_id)}, {"$set": category_data.model_dump()})
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
