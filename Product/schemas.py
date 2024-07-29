from pydantic import BaseModel

class Product(BaseModel):
    name: str
    description: str
    price: int

#Response body for Seller
class DisplaySeller(BaseModel):
    username: str
    email: str
    class Config:
        orm_mode = True

# Display only specific details as response body
class DisplayProduct(BaseModel):
    name: str
    description: str
    # Disaplaying seller class details
    seller: DisplaySeller
    class Config:
        orm_mode = True

class Seller(BaseModel):
    username: str
    email: str
    password: str
