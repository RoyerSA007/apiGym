from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session, engine, Base
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
import io


#from middlewares.jwt_bearer import JWTBearer
# from services.categoria import CategoriaService

from schemas.user import User
from services.user import UserService
from models.user import User as UserModel
#--------------------------------------------------------
from schemas.exercises import Ejercicio
from services.exercise import EjercicioService
from models.exercises import Ejercicio as EjercicioModel
#--------------------------------------------------------
from schemas.excerciseEntry import ExerciseEntry
from services.excerciseEntry import ExcerciseEntryService
from models.exerciseEntries import EntradaEjercicio as EntradaEjercicioModel



exerciseEntry_router = APIRouter()

def get_next_id():
    db = Session()
    max_id = db.query(func.max(EntradaEjercicioModel.id_en)).scalar()
    db.close()
    return (max_id or 0) + 1




@exerciseEntry_router.get('/excercise_weights', tags=['excercise_entry'], response_model=List[float])
def get_weights(user_id: int, exercise_id: int) -> List[float]:
    db = Session()
    weights = ExcerciseEntryService(db).get_weights_by_user_and_exercise(user_id, exercise_id)
    return weights


@exerciseEntry_router.get('/excercise_reps', tags=['excercise_entry'], response_model=List[float])
def get_reps(user_id: int, exercise_id: int) -> List[float]:
    db = Session()
    reps = ExcerciseEntryService(db).get_reps_by_user_and_exercise(user_id, exercise_id)
    return reps

@exerciseEntry_router.get('/excercise_entry', tags=['excercise_entry'], response_model=List[ExerciseEntry], status_code=200)
def get_AllEntradasEjercicios() -> List[ExerciseEntry]:
    db = Session()
    result = ExcerciseEntryService(db).get_entradasEjercicio()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@exerciseEntry_router.get('/excercise_entry/{id_en}', tags=['excercise_entry'], response_model=ExerciseEntry)
def get_OneEntradaEjercicio(id_en: int = Path(ge=1, le=2000)) -> ExerciseEntry:
    db = Session()
    result = ExcerciseEntryService(db).get_entradaEjercicio(id_en)
    if not result:
        return JSONResponse(status_code=404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@exerciseEntry_router.post('/excercise_entry', tags=['excercise_entry'], response_model=dict)
def create_entradaEjercicio(entrada : ExerciseEntry) -> dict:
    db = Session()
    entrada.id_en = get_next_id() 
 # Aquí llamamos al servicio para crear la entrada
    try:
        ExcerciseEntryService(db).create_entradaEjercicio(entrada)
    except HTTPException as e:
        # Si se lanza una HTTPException, pasamos la información al cliente
        raise e  # Esto automáticamente devuelve el código de estado y el detalle

    return JSONResponse(status_code=201, content={'message': "Se agregó la bitácora de ejercicio"})

@exerciseEntry_router.delete('/excercise_entry/{id_en}', tags=['excercise_entry'])
def delete_EntradaEjercicio(id_en: int):
    db = Session()
    result = db.query(EntradaEjercicioModel).filter(EntradaEjercicioModel.id_en == id_en).first()
    
    ExcerciseEntryService(db).delete_EntradaEjercicio(id_en)

    return JSONResponse(status_code=200, content={"message": "Se ha Eliminado la bitacora"})

@exerciseEntry_router.get('/excercise_entries_by_user/{user_id}', tags=['excercise_entry'], response_model=List[ExerciseEntry])
def get_excercises_by_user(user_id: int):
    db = Session()

    entries = ExcerciseEntryService(db).get_excercises_by_user(user_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(entries))

@exerciseEntry_router.get('/excercise_entries_user/{user_id}', tags=['excercise_entry'], response_model=List[ExerciseEntry])
def get_all_entries_by_user(user_id: int):
    db = Session()

    entries = ExcerciseEntryService(db).get_all_entries_by_user(user_id)
    return JSONResponse(status_code=200, content=jsonable_encoder(entries))


@exerciseEntry_router.get("/weights_graph", tags=['excercise_entry'], response_class=StreamingResponse)
async def get_weights_graph(user_id: int, exercise_id: int):
    # Obtener los pesos y fechas usando el servicio
    db = Session()
    entries = ExcerciseEntryService(db).get_weights_by_user_and_exercise_graph(user_id, exercise_id)

    if not entries:
        raise HTTPException(status_code=404, detail="No se encontraron pesos para el usuario y ejercicio especificados")

    # Separar pesos y fechas
    weights, dates = zip(*entries)  # Desempaquetar las tuplas

    # Crear la gráfica de los pesos con fechas en el eje X
    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights, marker='o', linestyle='-', color='b')
    plt.title('Pesos Registrados a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Peso (kg)')
    plt.xticks(rotation=45)  # Rotar las fechas para mejor legibilidad
    plt.grid()

    # Guardar la gráfica en un objeto BytesIO
    img_byte_arr = io.BytesIO()
    plt.savefig(img_byte_arr, format='png')
    img_byte_arr.seek(0)
    plt.close()  # Cerrar la figura para liberar memoria

    return StreamingResponse(img_byte_arr, media_type='image/png')

@exerciseEntry_router.get("/reps_graph", tags=['excercise_entry'], response_class=StreamingResponse)
async def get_reps_graph(user_id: int, exercise_id: int):
    # Obtener los pesos y fechas usando el servicio
    db = Session()
    entries = ExcerciseEntryService(db).get_reps_by_user_and_exercise_graph(user_id, exercise_id)

    if not entries:
        raise HTTPException(status_code=404, detail="No se encontraron pesos para el usuario y ejercicio especificados")

    # Separar pesos y fechas
    reps, dates = zip(*entries)  # Desempaquetar las tuplas

    # Crear la gráfica de los pesos con fechas en el eje X
    plt.figure(figsize=(10, 5))
    plt.plot(dates, reps, marker='o', linestyle='-', color='b')
    plt.title('Reps Registradas a lo Largo del Tiempo')
    plt.xlabel('Fecha')
    plt.ylabel('Repetciones')
    plt.xticks(rotation=45)  # Rotar las fechas para mejor legibilidad
    plt.grid()

    # Guardar la gráfica en un objeto BytesIO
    img_byte_arr = io.BytesIO()
    plt.savefig(img_byte_arr, format='png')
    img_byte_arr.seek(0)
    plt.close()  # Cerrar la figura para liberar memoria

    return StreamingResponse(img_byte_arr, media_type='image/png')

