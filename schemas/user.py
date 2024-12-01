from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=2, max_length=75)
    email: str = Field(min_length=2, max_length=75)
    password: str = Field(min_length=2, max_length=55)

    class Config:
        json_schema_extra = {
            "example":{
                "id": 1,
                "name":"Federico",
                "email": "fede@gmail.com",
                "password": "12345"
            }
        }

class LoginRequest(BaseModel):
    email: str = Field(..., min_length=2, max_length=75, example="eliseo@gmail.com")
    password: str = Field(..., min_length=2, max_length=55, example="Eps77648")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "eliseo@gmail.com",
                "password": "Eps77648"
            }
        }

class LoginResponse(BaseModel):
    userId: int
    isLogged: bool
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "userId": 1,
                "isLogged": True,
                "message": "Bienvenido"
            }
        }