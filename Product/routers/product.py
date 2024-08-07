from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.params import Depends
from ..database import get_db
from ..import models, schemas
from typing import List
from fastapi import FastAPI,status, Response, HTTPException


router = APIRouter(
    tags=['Products'],
    prefix='/product'
)

@router.delete('/{id}')
def deleteProduct(id, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Product deleted'}


@router.get('/', response_model=List[schemas.DisplayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products

@router.get('/{id}', response_model=schemas.DisplayProduct)
def product(id, response: Response, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    return product

@router.put('/{id}')
def updateProduct(id, request: schemas.Product, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    # if product is not found then exit
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return {'Product updated successfully'}

@router.post('/', status_code=status.HTTP_201_CREATED)
def add(request: schemas.Product, db: Session = Depends(get_db)):
    # creating a new product by using model.py
    new_product = models.Product(name=request.name, description=request.description, price=request.price, seller_id=1)
    # insert obj into database, commit it, refresh it
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request
