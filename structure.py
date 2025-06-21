from pydantic import BaseModel, Field , EmailStr, constr
import re



class User(BaseModel):
    name : str = Field(...,regex=r"^(\+65)?[689]\d{7}$")
    email: EmailStr = Field(...,max_length = 50)
    password : str = Field(...,min_length=3, max_length=15,regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$")   #one lowercase, uppercase, digit and special char, min8
    phone : int





