from pydantic import BaseModel

class AdminRegister(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class AdminLogin(BaseModel):
    email: str
    password: str

class AdminDetails(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    user_id: str

class Update(BaseModel):
    title: str
    category: str
    content: str
    date: str
    author: str
    image: str
    website_link: str = None
    document_link: str = None
    video_link: str = None

class BusinessForm(BaseModel):
    company_name: str
    contact_person: str
    email: str
    mobile: str
    country: str
    details: str

class Catalogue(BaseModel):
    catalogue_title: str
    catalogue_description: str
    url_link: str

class Category(BaseModel):
    category_name: str
    category_rank: int
    category_image: str
    commodities: list = []
    created_on: str

class Commodity(BaseModel):
    commodity_category: str
    commodity_name: str
    commodity_image: str
    created_on: str
    description: str
    specification: dict
    quality: str
    packaging_details: str
    FAQ: list
    countries_importing: list
    countries_exporting: list
    commodity_gallery: list
    past_shipment: dict

class ContactForm(BaseModel):
    full_name: str
    purpose: str
    message: str
    email: str
    mobile: str
    country: str

class GalleryItem(BaseModel):
    gallery_title: str
    images: list

class Gallery(BaseModel):
    _id: str
    gallery_title: str
    images: list

class Testimonial(BaseModel):
    testimonial_image: str
    person_name: str
    designation: str
    company: str
    content: str
    rating: int

class Tradeshow(BaseModel):
    tradeshow_image: str
    tradeshow_name: str
    url_link: str