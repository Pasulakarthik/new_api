from sqlalchemy import Column , String , Integer, ForeignKey
from app.database import Base

class User(Base):
    __tablename__ = "UserInfo"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String)
    password = Column(String)
    role = Column(String)

class Product(Base):
    __tablename__ = "ProductInfo"
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    model = Column(String,nullable=False)
    brand = Column(String,nullable=False)
    category = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    stock = Column(Integer,nullable=False)
    
class Cart(Base):
    __tablename__ = "CartInfo"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    model = Column(String,nullable=False)
    brand = Column(String,nullable=False)
    category = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    quantity = Column(Integer , default=1)
    user_id = Column(Integer,ForeignKey("UserInfo.id"))
    Product_id = Column(Integer,ForeignKey("ProductInfo.id"))

class Order(Base):
    __tablename__ = "OrderInfo"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    model = Column(String,nullable=False)
    brand = Column(String,nullable=False)
    category = Column(String,nullable=False)
    price = Column(Integer,nullable=False)
    quantity = Column(Integer , default=1)
    user_id = Column(Integer,ForeignKey("UserInfo.id"))
    Product_id = Column(Integer,ForeignKey("ProductInfo.id"))    