def individual_serial(field)-> dict:
    return{
        "id": str(field.get("_id")),
        "catalogue_title": field.get("catalogue_title"),
        "catalogue_description": field.get("catalogue_description"),
        "image_url": field.get("image_url"),
        "pdf_url": field.get("pdf_url"),
    }

def list_serial(fields) -> list:
    return [individual_serial(field) for field in fields]