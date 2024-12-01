from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session, engine, Base
from models.user import User as UserModel
from fastapi.encoders import jsonable_encoder
from services.user import UserService
from sqlalchemy import func

#from middlewares.jwt_bearer import JWTBearer
# from services.categoria import CategoriaService
from schemas.user import User,LoginRequest,LoginResponse
# from models.categoria import Categoria as CategoriaModel

user_router = APIRouter()

def get_next_id():
    db = Session()
    max_id = db.query(func.max(UserModel.id)).scalar()
    db.close()
    return (max_id or 0) + 1

@user_router.get('/users', tags=['users'], response_model=List[User], status_code=200)
def get_users() -> List[User]:
    db = Session()
    result = UserService(db).get_Usuarios()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@user_router.get('/userById/{id}', tags=['users'], response_model=User)
def get_user(id: int = Path(ge=1, le=2000)) -> User:
    db = Session()
    result = UserService(db).get_user(id)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@user_router.post('/users', tags=['users'], response_model=dict)
def create_user(users : User) -> dict:
    db = Session()

    users.id = get_next_id()
    UserService(db).create_usuario(users)

    return JSONResponse(status_code=200, content={'message': "Se agregó el usuario"})

@user_router.delete('/users/{id}', tags=['users'])
def delete_user(id: int):
    db = Session()
    result = db.query(UserModel).filter(UserModel.id == id).first()
    
    UserService(db).delete_user(id)

    return JSONResponse(status_code=200, content={"message": "Se ha Eliminado el Usuarui"})

# @user_router.get('/authenticate', tags=['users'])
# def authenticate_user(email:str,password:str):
#     db = Session()
#     result = UserService.authenticate_user(email,password)

#     if result == True:
#         return JSONResponse(status_code=200, content={"message": "Usuario aceptado"})
#     else:
#         return JSONResponse(status_code=400, content={"message": "Usuario Denegado"})

# @user_router.get('/authenticate', tags=['users'])
# def authenticate_user(email:str,password:str):
#     db = Session()
#     message,result = UserService(db).authenticate_user(email,password)

#     if result:
#         return JSONResponse(status_code=200, content={"message": "Usuario aceptado"})
#     else:
#         return JSONResponse(status_code=400, content={"message": "Usuario Denegado"})
    
@user_router.post("/login", tags=['users'],response_model=LoginResponse)
def login(login_request: LoginRequest):
    db = Session()
    result = UserService(db).authenticate_user(login_request)
    return result

