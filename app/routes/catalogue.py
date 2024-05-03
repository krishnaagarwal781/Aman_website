from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from bson import ObjectId

from app.models.models import *
from app.config.private import *

# Define Pydantic models for request and response


# Initialize FastAPI app
catalogueRouter = APIRouter()

# Catalogue endpoints
@catalogueRouter.get("/catalogue/all-catalogue", response_model=list[Catalogue], tags=['Catalogue Routes'])
async def get_all_catalogues():
    coll = db["catalogues"]
    catalogues = list(coll.find({}, {"_id": 0}))
    return catalogues

@catalogueRouter.post("/catalogue/create-catalogue", response_model=Catalogue, tags=['Catalogue Routes'])
async def create_catalogue(catalogue: Catalogue):
    coll = db["catalogues"]
    result = coll.insert_one(catalogue.dict())
    created_catalogue = coll.find_one({"_id": result.inserted_id}, {"_id": 0})
    return created_catalogue

@catalogueRouter.patch("/catalogue/edit-catalogue/{catalogue_id}", response_model=Catalogue, tags=['Catalogue Routes'])
async def edit_catalogue(catalogue_id: str, catalogue_data: Catalogue):
    coll = db["catalogues"]
    coll.update_one({"_id": ObjectId(catalogue_id)}, {"$set": catalogue_data.dict()})
    updated_catalogue = coll.find_one({"_id": ObjectId(catalogue_id)}, {"_id": 0})
    if updated_catalogue:
        return updated_catalogue
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")

@catalogueRouter.post("/catalogue/delete-catalogue/{catalogue_id}", tags=['Catalogue Routes'])
async def delete_catalogue(catalogue_id: str):
    coll = db["catalogues"]
    result = coll.delete_one({"_id": ObjectId(catalogue_id)})
    if result.deleted_count == 1:
        return {"message": "Catalogue deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")
