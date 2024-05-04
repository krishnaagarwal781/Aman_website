def individual_serial(field)-> dict:
    return{
        "id": str(field.get("_id")),
        "company_name": field.get("company_name"),
        "contact_person": field.get("contact_person"),
        "email": field.get("email"),
        "mobile": field.get("mobile"),
        "city": field.get("city"),
        "state": field.get("state"),
        "country": field.get("country"),
        "address": field.get("address"),
        "details": field.get("details"),
    }

def list_serial(fields) -> list:
    return [individual_serial(field) for field in fields]