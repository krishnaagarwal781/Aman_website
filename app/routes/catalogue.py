from fastapi import FastAPI, HTTPException, APIRouter, File, UploadFile
from fastapi.responses import FileResponse
from bson import ObjectId
import cloudinary
import cloudinary.uploader

from app.models.models import *
from app.config.private import *
from app.schemas.catalogue_schema import *

catalogueRouter = APIRouter()

# Catalogue endpoints


@catalogueRouter.post("/catalogue/create-catalogue", tags=['Catalogue Routes'])
async def create_catalogue(catalogue_title: str, catalogue_description: str, image: UploadFile = File(...), pdf: UploadFile = File(...)):
    # Upload image and PDF files to Cloudinary
    image_upload = cloudinary.uploader.upload(image.file, folder="Rose/Catalogues/Image")
    # pdf_upload = cloudinary.uploader.upload(pdf.file, resource_type="raw", folder="Rose/Catalogues")
    pdf_upload = cloudinary.uploader.upload(pdf.file, resource_type="auto", folder="Rose/Catalogues/PDF")

    # Insert links into MongoDB document
    document = {
        "catalogue_title": catalogue_title,
        "catalogue_description": catalogue_description,
        "image_url": image_upload["secure_url"],
        "pdf_url": pdf_upload["secure_url"]
    }
    result = catalogues_collection.insert_one(document)

    return {"message": "Catalogue created successfully", "catalogue_id": str(result.inserted_id)}

    # result = catalogues_collection.insert_one(catalogue.model_dump())
    # return {"catalogue_id": str(result.inserted_id)}

# @catalogueRouter.post("/catalogue/create-catalogue", tags=['Catalogue Routes'])
# async def create_catalogue(catalogue: Catalogue):
#     result = catalogues_collection.insert_one(catalogue.model_dump())
#     return {"catalogue_id": str(result.inserted_id)}

@catalogueRouter.patch("/catalogue/edit-catalogue/{catalogue_id}", tags=['Catalogue Routes'])
async def edit_catalogue(catalogue_id: str, catalogue_title: Optional[str] = None, catalogue_description: Optional[str] = None):
    catalogue = catalogues_collection.find_one({"_id": ObjectId(catalogue_id)})
    if catalogue:
        # Update the title and description if provided
        update_data = {}
        if catalogue_title is not None:
            update_data["catalogue_title"] = catalogue_title
        if catalogue_description is not None:
            update_data["catalogue_description"] = catalogue_description

        # Perform the update operation
        catalogues_collection.update_one(
            {"_id": ObjectId(catalogue_id)},
            {"$set": update_data}
        )

        return {"message": "Catalogue updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")


@catalogueRouter.patch("/catalogue/update-catalogue-image/{catalogue_id}", tags=['Catalogue Routes'])
async def update_catalogue_image(catalogue_id: str, image: UploadFile = File(...)):
    # Find the catalogue document in the database
    catalogue = catalogues_collection.find_one({"_id": ObjectId(catalogue_id)})
    if catalogue:
        # Upload the new image to Cloudinary
        upload_result = cloudinary.uploader.upload(image.file, resource_type="auto", folder='Rose/Catalogues/Image')
        # Get the new image URL
        new_image_url = upload_result["secure_url"]
        
        # Update the image URL in the catalogue document
        catalogues_collection.update_one(
            {"_id": ObjectId(catalogue_id)},
            {"$set": {"image_url": new_image_url}}
        )

        return {"message": "Catalogue image updated successfully", "new_image_url": new_image_url}
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")


@catalogueRouter.patch("/catalogue/update-catalogue-pdf/{catalogue_id}", tags=['Catalogue Routes'])
async def update_catalogue_pdf(catalogue_id: str, pdf_file: UploadFile = File(...)):
    # Find the catalogue document in the database
    catalogue = catalogues_collection.find_one({"_id": ObjectId(catalogue_id)})
    if catalogue:
        if pdf_file.filename.endswith('.pdf'):
            # Upload the new PDF file to Cloudinary
            upload_result = cloudinary.uploader.upload(pdf_file.file, resource_type="auto", folder='Rose/Catalogues/PDF')
            # Get the new PDF URL
            new_pdf_url = upload_result["secure_url"]
            
            # Update the PDF URL in the catalogue document
            catalogues_collection.update_one(
                {"_id": ObjectId(catalogue_id)},
                {"$set": {"pdf_url": new_pdf_url}}
            )

            return {"message": "Catalogue PDF updated successfully", "new_pdf_url": new_pdf_url}
        else:
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")




@catalogueRouter.delete("/catalogue/delete-catalogue/{catalogue_id}", tags=['Catalogue Routes'])
async def delete_catalogue(catalogue_id: str):
    result = catalogues_collection.delete_one({"_id": ObjectId(catalogue_id)})
    if result.deleted_count == 1:
        return {"message": "Catalogue deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Catalogue not found")

@catalogueRouter.get("/catalogue/get-catalogue", tags=['Catalogue Routes'])
async def get_catalogue(catalogue_id: str):
    catalogue = catalogues_collection.find_one({"_id": ObjectId(catalogue_id)})
    return individual_serial(catalogue)

@catalogueRouter.get("/catalogue/get-all-catalogues", tags=['Catalogue Routes'])
async def get_all_catalogues():
    catalogues = catalogues_collection.find()
    return list_serial(catalogues)