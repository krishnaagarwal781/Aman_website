from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AdminRegister(BaseModel):
    full_name: str
    email: str
    password: str

class AdminLogin(BaseModel):
    email: str
    password: str


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
    mobile: int
    city: str
    state: str
    country: str
    address: str
    details: str

class Catalogue(BaseModel):
    catalogue_title: str
    catalogue_description: str
    image_url: str
    pdf_url: str

class Category(BaseModel):
    category_name: str
    category_rank: int
    category_image: str
    # commodities: list = []
    commodities: Optional[List] = []
    created_on: datetime

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
    images: Optional[List] = []

class Gallery(BaseModel):
    _id: str
    gallery_title: str
    images: Optional[List] = []

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