from fastapi import APIRouter
from ..import schemas, models
from sqlalchemy.orm import Session
from fastapi.params import Depends
from passlib.context import CryptContext
from ..database import get_db


router = APIRouter(
    tags=['Seller']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/seller', response_model=schemas.DisplaySeller)
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    # Hashing and encrypting password
    hashed_pwd = pwd_context.hash(request.password)
    new_seller = models.Seller(username = request.username, email = request.email, password = hashed_pwd)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller

