from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, field_validator
from database import users_collection
import bcrypt
from datetime import datetime, timedelta
import jwt



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
        if not re.search(r"[A-Z]", pw):
            raise ValueError("Password must include an uppercase letter")
        if not re.search(r"[a-z]", pw):
            raise ValueError("Password must include a lowercase letter")
        if not re.search(r"\d", pw):
            raise ValueError("Password must include a digit")
        if not re.search(r"[@$!%*?&]", pw):
            raise ValueError("Password must include a special character (@$!%*?&)")
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

@router.post("/login")
def login(user: UserRegister):
    found = users_collection.find_one({"email": user.email})
    if not found or not Passwords.verify_password(str(user.password), str(found["password"])):
        return {"msg": "wrong email or password"}
    
    access_token = create_token(data={"email": found["email"]})

    return {"msg": "Login successful", " token": access_token}


token_expiry = 30
secret_key = 'xxyyzz'
algorithm = 'RS256' # or 'HS256'  tocheck


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=token_expiry)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm)


@router.get("/all-users")
def get_all_users():
    users = list(users_collection.find({}, {"_id": 0}))  
    return users

