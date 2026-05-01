from fastapi import APIRouter , Depends , status , HTTPException, Form,Request, BackgroundTasks 
from fastapi.responses import RedirectResponse,HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Product , User , Cart , Order
from .user import get_current_user 
import logging
from app.config import env


router = APIRouter(
    prefix="/Shopping",
    tags=["Shopping"]
)

#?----------Cart-----------


@router.post("/AddToCart")
def AddToCart(
    request: Request,
    quantity:int = Form(...),
    product_id:int = Form(...),
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        template = env.get_template("addcartmes.html")
        return HTMLResponse(
        template.render(request=request, msg="Product Not Found")
        )

    
    if product.stock <= quantity:
        template = env.get_template("addcartmes.html")
        return HTMLResponse(
        template.render(request=request, msg="Insufficient stock")
        )
    
    existing = db.query(Cart).filter(
        Cart.user_id == current_user.id,
        Cart.Product_id == product.id
    ).first()

    if existing:
        template = env.get_template("addcartmes.html")
        return HTMLResponse(
        template.render(request=request, msg="Product Already Present")
        )
        
    else:

        new = Cart(
            name = product.name,
            model = product.model,
            brand = product.brand,
            category = product.category,
            price = product.price,
            quantity = quantity,
            user_id = current_user.id,
            Product_id = product.id
            )
    
        db.add(new)
        db.commit()
        db.refresh(new)

    product.stock -= quantity
    
    db.commit()

    template = env.get_template("addcartmes.html")
    return HTMLResponse(
    template.render(request=request, msg="Product added to cart successfully ✅")
    )


@router.get("/cart")
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).all()

    if not cart:
        return {"message": "Cart is empty", "items": []}

    return cart

@router.post("/remove_cart")
def delete_cart(
    request : Request,
    id: int = Form(...),
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    cart = db.query(Cart).filter(Cart.id == id).first()
    if not cart:
        template = env.get_template("deletecartmes.html")
        return HTMLResponse(
        template.render(request=request, msg="Product Not Found")
        )
    
    db.query(Product).filter(Product.id == Cart.Product_id).update({Product.stock: Product.stock + Cart.quantity})


    db.delete(cart)
    db.commit()
    
    template = env.get_template("deletecartmes.html")
    return HTMLResponse(
    template.render(request=request, msg="Cart Item Deleted")
    )

#?----------Order-----------

def order(email:str,current_user: User = Depends(get_current_user) ):
    logging.info(f"order placed by the user with  gmail {email}")

def deleteorder(email:str,current_user: User = Depends(get_current_user) ):
    logging.info(f"order deleted by the user with  gmail {email}")

@router.post("/order")
def Place_Order(background_tasks:BackgroundTasks,
    request : Request,
    quantity:int = Form(...),
    product_id:int = Form(...),
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    existing = db.query(Order).filter(Order.Product_id == product_id,Order.user_id == current_user.id).first()


    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        template = env.get_template("addordermes.html")
        return HTMLResponse(
        template.render(request=request, msg="Product Not Found")
        )
    
    
    if product.stock < quantity:
        template = env.get_template("addordermes.html")
        return HTMLResponse(
        template.render(request=request, msg="Insufficient Stock")
        )
        

    new = Order(
        name = product.name,
        model = product.model,
        brand = product.brand,
        category = product.category,
        price = product.price,
        quantity = quantity,
        user_id = current_user.id,
        Product_id = product.id
        )
        

    if existing:
        template = env.get_template("addordermes.html")
        return HTMLResponse(
        template.render(request=request, msg="Product already present in orders")
        )
    
    
    db.query(Product).filter(Product.id == product_id).update({Product.stock: Product.stock - quantity})


    
    db.add(new)
    db.commit()
    db.refresh(new)

    background_tasks.add_task(order, current_user.email)

    template = env.get_template("addordermes.html")
    return HTMLResponse(
    template.render(request=request, msg="Order Placed Successful")
    )
    




@router.get("/get_order")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.user_id == current_user.id
    ).all()

    if not order:
        return {"message": "No  Orders yet", "items": []}

    return order


@router.post("/remove_orders")
def delete_order(
    background_tasks:BackgroundTasks,
    request : Request,
    id: int = Form(...),
    db:Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    order = db.query(Order).filter(
        Order.id == id,
        Order.user_id == current_user.id
        ).first()
    
    if not order:
        template = env.get_template("deleteordermes.html")
        return HTMLResponse(
        template.render(request=request, msg=f"No order with this id {id}")
        )
    
    db.query(Product).filter(Product.id == Order.Product_id).update({Product.stock: Product.stock + Order.quantity})


    db.delete(order)
    db.commit()
    background_tasks.add_task(order, current_user.email)

    template = env.get_template("deleteordermes.html")
    return HTMLResponse(
    template.render(request=request, msg="Order Removed")
    )
