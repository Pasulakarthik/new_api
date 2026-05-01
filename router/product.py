from fastapi import APIRouter , Depends , status , HTTPException, Form,Request , Query
from fastapi.responses import RedirectResponse , HTMLResponse
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.model import Product , User
from .user import get_current_user 
from app.config import env



router = APIRouter(
    prefix="/Product",
    tags=["Product"]
)


@router.get("/filter", tags=["Filter"])
def Filter_products(
    request : Request,
    min_price: Optional[int] = Query(None, ge=0),
    max_price: Optional[int] = Query(None, ge=0),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(
                status_code=400,
                detail="min_price cannot be greater than max_price"
            )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    products = query.all()

    template = env.get_template("filterproducts.html")
    return HTMLResponse(
        template.render(request=request, products=products)
    )




@router.get("/")
def get_products(db:Session = Depends(get_db)):
    products = db.query(Product).all()

    return products

@router.post("/create_product")
def create_product(
    request : Request,
    db:Session = Depends(get_db),
    name : str = Form(...), 
    model : str = Form(...),
    brand : str = Form(...),
    category : str = Form(...),
    price : int = Form(...),
    stock : int = Form(...),
    current_user: User = Depends(get_current_user)               
    ):

    if current_user.role != "admin":
        template = env.get_template("createmes.html")
        return HTMLResponse(
        template.render(request=request, msg="Admins only")
        )

    product = db.query(Product).filter(Product.name == name).first()
    if product:
        template = env.get_template("createmes.html")
        return HTMLResponse(
        template.render(request=request, msg="Product already Present")
        )
       
    new = Product(
    name = name,
    model = model,
    brand = brand,
    category = category,
    price = price,
    stock = stock
    )

    db.add(new)
    db.commit()
    db.refresh(new)

    template = env.get_template("createmes.html")
    return HTMLResponse(
    template.render(request=request, msg="Product added successful")
    )

@router.post("/update")
def update_product(request : Request,
    id: str = Form(...),
    name : str = Form(...), 
    model : str = Form(...),
    brand : str = Form(...),
    category : str = Form(...),
    price : int = Form(...),
    stock : int = Form(...), 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.role != "admin":
        template = env.get_template("updatemes.html")
        return HTMLResponse(
        template.render(request=request, msg="Admin only")
        )
    
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        template = env.get_template("updatemes.html")
        return HTMLResponse(
        template.render(request=request, msg=f"Product with id {id} Not found")
        )

    product.name = name
    product.model = model
    product.brand = brand
    product.category = category
    product.price = price
    product.stock = stock

    db.commit()

    template = env.get_template("updatemes.html")
    return HTMLResponse(
    template.render(request=request, msg="Product Updated")
    )
    


@router.post("/delete")
def delete_product(
    request:Request,
    id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    if current_user.role != "admin":
        template = env.get_template("deletemes.html")
        return HTMLResponse(
        template.render(request=request, msg="Admin only")
        )
    
    user = db.query(User).filter(User.email == current_user.email).first()
    
    if not user:
        template = env.get_template("deletemes.html")
        return HTMLResponse(
        template.render(request=request, msg="User Not Found")
        )
    
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        template = env.get_template("deletemes.html")
        return HTMLResponse(
        template.render(request=request, msg=f"Product with id {id} Not found")
        )

    db.delete(product)
    db.commit()

    template = env.get_template("deletemes.html")
    return HTMLResponse(
    template.render(request=request, msg="Product Deleted")
    )
    
     