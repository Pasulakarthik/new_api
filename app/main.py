from fastapi import FastAPI, Depends , HTTPException, status , Request
from app.database import Base , engine , get_db
from app.model import *
from router import user, product, shopping
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from router.user import get_current_user
from app.config import templates, BASE_DIR


app = FastAPI()

Base.metadata.create_all(bind=engine)



@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/get_user", response_class=HTMLResponse)
def user_page(request: Request,db:Session = Depends(get_db)):
    user = db.query(User).all()
    return templates.TemplateResponse("users.html", {"request": request , "user":user})

@app.post("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/regmes", response_class=HTMLResponse)
def Register_page(request: Request):
    return templates.TemplateResponse("regmes.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("log.html", {"request": request})

@app.get("/logmes", response_class=HTMLResponse)
def Login_page(request: Request):
    return templates.TemplateResponse("logmes.html", {"request": request})

#!---------Products------------

@app.get("/store", response_class=HTMLResponse)
def store_page(request: Request):
    return templates.TemplateResponse("store.html", {"request": request})

@app.get("/filter", response_class=HTMLResponse)
def filter_page(request: Request):
    return templates.TemplateResponse("filter.html", {"request": request})

@app.get("/filterproducts", response_class=HTMLResponse)
def Filter_page(request: Request):
    return templates.TemplateResponse("filterproducts.html", {"request": request})

@app.get("/get_product", response_class=HTMLResponse)
def product_page(request: Request,db:Session = Depends(get_db)):
    product = db.query(Product).all()
    return templates.TemplateResponse("products.html", {"request": request , "product":product})

@app.post("/create_product", response_class=HTMLResponse)
def create_product_page(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

@app.get("/createmes", response_class=HTMLResponse)
def Create_page(request: Request):
    return templates.TemplateResponse("createmes.html", {"request": request})


@app.post("/update", response_class=HTMLResponse)
def update_product_page(request: Request):
    return templates.TemplateResponse("updates.html", {"request": request})

@app.get("/updatemes", response_class=HTMLResponse)
def Update_page(request: Request):
    return templates.TemplateResponse("updatemes.html", {"request": request})

@app.post("/delete", response_class=HTMLResponse)
def delete_product_page(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

@app.get("/deletemes", response_class=HTMLResponse)
def Delete_page(request: Request):
    return templates.TemplateResponse("deletemes.html", {"request": request})

#!---------Shopping------------


@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    return templates.TemplateResponse("cart.html", {"request": request , "cart":cart})

@app.post("/AddToCart", response_class=HTMLResponse)
def addtocart_page(request: Request):
    return templates.TemplateResponse("addtocart.html", {"request": request})

@app.get("/addcartmes", response_class=HTMLResponse)
def Addtocart_page(request: Request):
    return templates.TemplateResponse("addcartmes.html", {"request": request})

@app.post("/remove_cart", response_class=HTMLResponse)
def delete_product_page(request: Request):
    return templates.TemplateResponse("deletecart.html", {"request": request})

@app.get("/deletecartmes", response_class=HTMLResponse)
def Delete_page(request: Request):
    return templates.TemplateResponse("deletecartmes.html", {"request": request})


@app.get("/get_order", response_class=HTMLResponse)
def order_page(request: Request,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    order = db.query(Order).filter(Order.user_id == current_user.id).all()
    return templates.TemplateResponse("order.html", {"request": request,"order":order})

@app.post("/order", response_class=HTMLResponse)
def addtoorder_page(request: Request):
    return templates.TemplateResponse("addtoorder.html", {"request": request})

@app.get("/addordermes", response_class=HTMLResponse)
def AddToOrder_page(request: Request):
    return templates.TemplateResponse("addordermes.html", {"request": request})

@app.post("/remove_order", response_class=HTMLResponse)
def delete_order_page(request: Request):
    return templates.TemplateResponse("deleteorder.html", {"request": request})

@app.get("/deleteorder", response_class=HTMLResponse)
def DeleteOrder_page(request: Request):
    return templates.TemplateResponse("deleteordermes.html", {"request": request})


app.include_router(user.router) 
app.include_router(product.router) 
app.include_router(shopping.router) 

