def individual_serial(field)-> dict:
    return{
        "id": str(field.get("_id")),
        "category_name": field.get("category_name"),
        "category_rank": field.get("category_rank"),
        "category_image": field.get("category_image"),
        "commodities": field.get("commodities"),
        "created_on": field.get("created_on"),
    }

def list_serial(fields) -> list:
    return [individual_serial(field) for field in fields]