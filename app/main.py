from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.config.private import *
from app.routes.admin import adminRouter as admin_app
from app.routes.business_form import businessRouter as business_form_app
from app.routes.catalogue import catalogueRouter as catalogue_app
from app.routes.categories import categoryRouter as categories_app
from app.routes.commodities import commodityRouter as commodities_app
from app.routes.contact_form import contactRouter as contact_form_app
from app.routes.gallery import galleryRouter as gallery_app
from app.routes.testimonials import testimonyRouter as testimonials_app
from app.routes.tradeshow import tradeshowRouter as tradeshow_app


app = FastAPI(
    title="Content Management System",
    description="Content Management System",
    version="1.0",
    docs_url="/api",
    redoc_url="/reapi",
)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin_app)
app.include_router(business_form_app)
app.include_router(catalogue_app)
app.include_router(categories_app)
app.include_router(commodities_app)
app.include_router(contact_form_app)
app.include_router(gallery_app)
app.include_router(testimonials_app)
app.include_router(tradeshow_app)