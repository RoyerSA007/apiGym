from config.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from pydantic import BaseModel



class User(Base):

    __tablename__="users"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    exercise_entries = relationship("EntradaEjercicio", back_populates="user")
    

# Clase para la solicitud de login
class LoginRequest(BaseModel):
    email: str
    password: str

# Clase para la respuesta de login
class LoginResponse(BaseModel):
    userId: int
    isLogged: bool
    message: str
    