from fastapi import APIRouter
from pydantic import BaseModel, EmailStr, field_validator
from ..database import users_collection
from bson import ObjectId

router = APIRouter()

class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, pw):
        import re
        if len(pw) < 8: return {"msg":"Min 8 chars"}
        if not re.search(r"[A-Z]", pw): return {"msg":"Must include uppercase"}
        if not re.search(r"[a-z]", pw): return {"msg": " Must include lowercase"}
        if not re.search(r"\d", pw): return {"msg":"Must include digit"}
        if not re.search(r"[@$!%*?&]", pw): return {"msg":"Must include special char"}
        return pw

@router.post("/register")
def register(user: UserRegister):
    if users_collection.find_one({"email": user.email}):
        return {"msg": "User exists"}
    users_collection.insert_one(user.model_dump())
    return {"msg": "User registered"}

@router.post("/login")
def login(user: UserRegister):
    found = users_collection.find_one({"email": user.email})
    if not found or found["password"] != user.password:
        return {"msg": "Not found"}
    return {"msg": "Login successful"}
