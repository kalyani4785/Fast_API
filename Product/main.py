import logging
from fastapi import FastAPI
from Product import models
from Product.database import engine
from .routers import product, seller

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fast API instance
app = FastAPI(
    # creating meta-data for Swagger
    title= "Products API",
    description= "Get details for all the products on our website",
    terms_of_service= "https://www.google.com",
    contact={
        "Developer Name": "Kalyani",
        "website": "https://www.google.com",
        "email": "demo@gmail.com"
    },
    license_info={
        'name': "XYZ",
        'url':"https://www.google.com"
    },
    # docs_url="/documentation",
    # redoc_url=None
)

# API router reference
app.include_router(product.router)
app.include_router(seller.router)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

