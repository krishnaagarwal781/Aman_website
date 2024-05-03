from fastapi import FastAPI, HTTPException, APIRouter
from bson import ObjectId

from app.models.models import *
from app.config.private import *

# Define Pydantic models for request and response


# Initialize FastAPI app
galleryRouter = APIRouter()

# Gallery endpoints
@galleryRouter.get("/gallery/all-gallery", response_model=list[Gallery], tags=['Gallery Routes'])
async def get_all_gallery():
    coll = db["gallery"]
    galleries = list(coll.find({}, {"_id": 1, "gallery_title": 1, "images": 1}))
    return galleries

@galleryRouter.post("/gallery/create-gallery", response_model=Gallery, tags=['Gallery Routes'])
async def create_gallery(gallery: GalleryItem):
    coll = db["gallery"]
    result = coll.insert_one(gallery.dict())
    created_gallery = coll.find_one({"_id": result.inserted_id})
    return {**created_gallery, "_id": str(created_gallery["_id"])}

@galleryRouter.patch("/gallery/edit-gallery/{gallery_id}", response_model=Gallery, tags=['Gallery Routes'])
async def edit_gallery(gallery_id: str, gallery_data: GalleryItem):
    coll = db["gallery"]
    coll.update_one({"_id": ObjectId(gallery_id)}, {"$set": gallery_data.dict()})
    updated_gallery = coll.find_one({"_id": ObjectId(gallery_id)})
    if updated_gallery:
        return {**updated_gallery, "_id": str(updated_gallery["_id"])}
    else:
        raise HTTPException(status_code=404, detail="Gallery not found")

@galleryRouter.post("/gallery/delete-gallery/{gallery_id}", tags=['Gallery Routes'])
async def delete_gallery(gallery_id: str):
    coll = db["gallery"]
    result = coll.delete_one({"_id": ObjectId(gallery_id)})
    if result.deleted_count == 1:
        return {"message": "Gallery deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Gallery not found")
