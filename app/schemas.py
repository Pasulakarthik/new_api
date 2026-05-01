from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:str

class login(BaseModel):
    email:EmailStr
    password:str

#!------------Product-----------
class CreateProduct(BaseModel):
    name:str
    category:str
    stock:int
    price:int
    brand:str
    model:str
    

class ProductIn(BaseModel):
    name:str
    category:str
    stock:int
    price:int
    brand:str
    model:str

class ProductOut(ProductIn):
    id:int
    class Config:
        from_attributes = True

class UpdateProduct(BaseModel):
    name:str
    category:str
    stock:int
    price:int
    brand:str
    model:str