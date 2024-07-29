import logging
from fastapi import FastAPI
from sqlalchemy.sql.functions import mode
from Product import schemas, models
from Product.database import engine
from Product.database import SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi import status, Response, HTTPException
from passlib.context import CryptContext

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

# Create the database tables
models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# gets database session & close it also(makes aconnection to database)
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


@app.delete('/product/{id}', tags=['Products'])
def deleteProduct(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Product deleted'}


@app.get('/products', response_model=List[schemas.DisplayProduct], tags=['Products'])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@app.get('/product/{id}', response_model=schemas.DisplayProduct, tags=['Products'])
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    return product

@app.put('/product/{id}', tags=['Products'])
def updateProduct(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    # if product is not found then exit
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return {'Product updated successfully'}

@app.post('/product', status_code=status.HTTP_201_CREATED, tags=['Products'])
def add(request: schemas.Product, db: Session = Depends(get_db)):
    # creating a new product by using model.py
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    # insert obj into database, commit it, refresh it
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


@app.post('/seller', response_model=schemas.DisplaySeller, tags=['Seller'])
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    # Hashing and encrypting password
    hashed_pwd = pwd_context.hash(request.password)
    new_seller = models.Seller(username = request.username, email = request.email, password = hashed_pwd)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller

