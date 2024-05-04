def individual_serial(field)-> dict:
    return{
        "id": str(field.get("_id")),
        "full_name": field.get("full_name"),
        "purpose": field.get("purpose"),
        "message": field.get("message"),
        "email": field.get("email"),
        "mobile": field.get("mobile"),
        "country": field.get("country"),
    }

def list_serial(fields) -> list:
    return [individual_serial(field) for field in fields]