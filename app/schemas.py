from pydantic import BaseModel, EmailStr

from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    # password limitado a 72 bytes pela especificação do bcrypt (aprox. 72 chars)
    password: constr(min_length=1, max_length=72)

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True