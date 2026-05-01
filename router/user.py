from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks,Form, Request
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from datetime import datetime , timedelta
from jose import JWTError, jwt
import logging
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app.model import User
from app.config import templates
from app.password import hash_password,pass_context,verify_password

router = APIRouter(
    prefix="/user",
    tags=["User"]
)





SECRET_KEY = "mykey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def login_mail(email:str):
    logging.info(f"Welcome to the e-commers store {email}")


# Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(request:Request, db:Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credential",headers={"www-Authenticate":"Bearer"})

    try:
        payload = jwt.decode(token , SECRET_KEY,algorithms=[ALGORITHM])
        name : str = payload.get("sub")
        
        if name is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
    user =db.query(User).filter(User.name == name).first()

    if user is None:
        raise HTTPException(status_code=401,detail="user not found")
    
    return user

def require_roles(allowed_roles:list[str]):
    def role_check(current_user: User = Depends(get_current_user)):
        user_role = current_user.role
        if user_role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not enough permission")
        
        return current_user
    return role_check

def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin only")
    
    return current_user

@router.post("/register")
def register(background_task:BackgroundTasks,
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    db:Session = Depends(get_db)):

    existing = db.query(User).filter(User.email== email).first()
    
    if existing:
        return templates.TemplateResponse("regmes.html", {"request": request, "msg":"Email already existed" })


    password = hash_password(password)

    new = User(
        name = name,
        email = email,
        password = password,
        role = role.lower()
    )

    db.add(new)
    db.commit()
    db.refresh(new)
    background_task.add_task(login_mail,email)


    return templates.TemplateResponse("regmes.html", {"request": request, "msg":"Registration Successful" })

@router.post("/login")
def login(request:Request,from_data:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.name == from_data.username).first()
    if not user:
        return templates.TemplateResponse("logmes.html", {"request": request, "msg":"Invalid User name" })
    if not pass_context.verify(from_data.password,user.password):
        return templates.TemplateResponse("logmes.html", {"request": request, "msg":"Invalid Password" })

    token_data = {"sub":user.name,"role":user.role}
    token = create_access_token(token_data)

    response = RedirectResponse("/store", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)

    return response

@router.get("/get_user")
def get_user(db:Session = Depends(get_db)):
    user = db.query(User).all()

    return db.query(User).all()