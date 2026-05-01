from fastapi import FastAPI, Depends , HTTPException, status , Request
from app.database import Base , engine , get_db
from app.model import *
from router import user, product, shopping
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from router.user import get_current_user
from app.config import env


app = FastAPI()

Base.metadata.create_all(bind=engine)



@app.get("/", response_class=HTMLResponse)
def home_page(request: Request):
    template = env.get_template("home.html")
    return HTMLResponse(template.render(request=request))

@app.get("/get_user", response_class=HTMLResponse)
def user_page(request: Request, db: Session = Depends(get_db)):
    user = db.query(User).all()
    
    template = env.get_template("users.html")
    return HTMLResponse(
        template.render(request=request, user=user)
    )


@app.post("/register", response_class=HTMLResponse)
def register_page(request: Request):
    template = env.get_template("signin.html")
    return HTMLResponse(
        template.render(request=request, user=user)
    )

@app.get("/regmes", response_class=HTMLResponse)
def Register_page(request: Request):
    template = env.get_template("regmes.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.post("/login", response_class=HTMLResponse)
def login_page(request: Request):
    template = env.get_template("log.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/logmes", response_class=HTMLResponse)
def Login_page(request: Request):
    template = env.get_template("logmes.html")
    return HTMLResponse(
        template.render(request=request)
    )

#!---------Products------------

@app.get("/store", response_class=HTMLResponse)
def store_page(request: Request):
    template = env.get_template("store.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/filter", response_class=HTMLResponse)
def filter_page(request: Request):
    template = env.get_template("filter.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/filterproducts", response_class=HTMLResponse)
def Filter_page(request: Request):
    template = env.get_template("filterproducts.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/get_product", response_class=HTMLResponse)
def product_page(request: Request,db:Session = Depends(get_db)):
    product = db.query(Product).all()
    template = env.get_template("products.html")
    return HTMLResponse(
        template.render(request=request, product=product)
    )

@app.post("/create_product", response_class=HTMLResponse)
def create_product_page(request: Request):
    template = env.get_template("add_product.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/createmes", response_class=HTMLResponse)
def Create_page(request: Request):
    template = env.get_template("createmes.html")
    return HTMLResponse(
        template.render(request=request)
    )


@app.post("/update", response_class=HTMLResponse)
def update_product_page(request: Request):
    template = env.get_template("updates.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/updatemes", response_class=HTMLResponse)
def Update_page(request: Request):
    template = env.get_template("updatemes.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.post("/delete", response_class=HTMLResponse)
def delete_product_page(request: Request):
    template = env.get_template("delete.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/deletemes", response_class=HTMLResponse)
def Delete_page(request: Request):
    template = env.get_template("deletemes.html")
    return HTMLResponse(
        template.render(request=request)
    )

#!---------Shopping------------


@app.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    template = env.get_template("cart.html")
    return HTMLResponse(
        template.render(request=request, cart=cart)
    )

@app.post("/AddToCart", response_class=HTMLResponse)
def addtocart_page(request: Request):
    template = env.get_template("addtocart.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/addcartmes", response_class=HTMLResponse)
def Addtocart_page(request: Request):
    template = env.get_template("addcartmes.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.post("/remove_cart", response_class=HTMLResponse)
def delete_product_page(request: Request):
    template = env.get_template("deletecart.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/deletecartmes", response_class=HTMLResponse)
def Delete_page(request: Request):
    template = env.get_template("deletecartmes.html")
    return HTMLResponse(
        template.render(request=request)
    )


@app.get("/get_order", response_class=HTMLResponse)
def order_page(request: Request,
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    order = db.query(Order).filter(Order.user_id == current_user.id).all()
    template = env.get_template("order.html")
    return HTMLResponse(
        template.render(request=request, order=order)
    )

@app.post("/order", response_class=HTMLResponse)
def addtoorder_page(request: Request):
    template = env.get_template("addtoorder.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/addordermes", response_class=HTMLResponse)
def AddToOrder_page(request: Request):
    template = env.get_template("addordermes.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.post("/remove_order", response_class=HTMLResponse)
def delete_order_page(request: Request):
    template = env.get_template("deleteorder.html")
    return HTMLResponse(
        template.render(request=request)
    )

@app.get("/deleteorder", response_class=HTMLResponse)
def DeleteOrder_page(request: Request):
    template = env.get_template("deleteordermes.html")
    return HTMLResponse(
        template.render(request=request)
    )


app.include_router(user.router) 
app.include_router(product.router) 
app.include_router(shopping.router) 

