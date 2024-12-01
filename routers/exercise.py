from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session, engine, Base
from models.exerciseEntries import Ejercicio as EjercicioModel
from fastapi.encoders import jsonable_encoder
from services.exercise import EjercicioService
from sqlalchemy import func
#from middlewares.jwt_bearer import JWTBearer
# from services.categoria import CategoriaService
from schemas.exercises import Ejercicio
# from models.categoria import Categoria as CategoriaModel

excercise_router = APIRouter()

def get_next_id():
    db = Session()
    max_id = db.query(func.max(EjercicioModel.id_ex)).scalar()
    db.close()
    return (max_id or 0) + 1

@excercise_router.get('/exercises', tags=['exercises'], response_model=List[Ejercicio], status_code=200)
def get_exercises() -> List[Ejercicio]:
    db = Session()
    result = EjercicioService(db).get_ejercicios()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@excercise_router.get('/exercises/{id_ex}', tags=['exercises'], response_model=Ejercicio)
def get_ejercicio(id_ex: int = Path(ge=1, le=2000)) -> Ejercicio:
    db = Session()
    result = EjercicioService(db).get_ejercicio(id_ex)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@excercise_router.post('/exercises', tags=['exercises'], response_model=dict)
def create_ejercicio(ejercicio : Ejercicio) -> dict:
    db = Session()

    ejercicio.id_ex = get_next_id()
    EjercicioService(db).create_ejercicio(ejercicio)

    return JSONResponse(status_code=200, content={'message': "Se agregó el ejercicio"})

@excercise_router.delete('/exercises/{id_ex}', tags=['exercises'])
def delete_ejercicio(id_ex: int):
    db = Session()
    result = db.query(EjercicioModel).filter(EjercicioModel.id_ex == id_ex).first()
    
    EjercicioService(db).delete_ejercicio(id_ex)

    return JSONResponse(status_code=200, content={"message": "Se ha Eliminado el Ejercicio"})
