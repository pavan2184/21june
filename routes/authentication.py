from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from database import users_collection
import bcrypt
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


token_expiry = 30
secret_key = 'xxyyzz'
algorithm = 'HS256' 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=token_expiry)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm = algorithm)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return payload.get("email") 


router = APIRouter()

class Passwords:
    @staticmethod
    def hash_password(password: str):
        pw_bytes = str(password).encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(pw_bytes, salt)
        return hash.decode('utf-8')
    
    @staticmethod
    def verify_password(plain: str, hashed: str) :
        user_bytes = plain.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')  
        return bcrypt.checkpw(user_bytes, hashed_bytes)


class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, pw):
        import re
        if len(pw) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"\d", pw):
            raise ValueError("Password must include a digit")
        if not re.search(r"[@$!%*?&]", pw):
            raise ValueError("Password must include a special character (@$!%*?&)")
        if not re.search(r"[A-Z]", pw):
            raise ValueError("Password must include an uppercase letter")
        if not re.search(r"[a-z]", pw):
            raise ValueError("Password must include a lowercase letter")
        return pw


@router.post("/register")
def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        return {"msg": "User exists"}
    
    user_data = {
        "email": user.email,
        "password": Passwords.hash_password(user.password)  
    }
    users_collection.insert_one(user_data)
    return {"msg": "User registered successfully"}

@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})
    if not user or not Passwords.verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_token(data={"email": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/all-users")
def get_all_users():
    users = list(users_collection.find({}, {"_id": 0}))  
    return users

