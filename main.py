from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from routers.user import user_router
from routers.exercise import excercise_router
from routers.excerciseEntry import exerciseEntry_router
from fastapi.middleware.cors import CORSMiddleware



from models.user import User  # Asegúrate de importar todos los modelos
from models.exercises import Ejercicio
from models.exerciseEntries import EntradaEjercicio


# from middlewares.error_handler import ErrorHandler


origins = [
    "http://localhost:51164",  # Frontend local (ajústalo según tu entorno)
    "http://127.0.0.1:3000",  # Otra posible dirección de desarrollo
    "http://localhost",  # Si estás usando emuladores de Android o iOS, agrega esta opción también.
    "http://127.0.0.1",  # Para emuladores también
]

app = FastAPI()
app.title = "Gym Buddy"
app.version = "0.0.1"

app.include_router(user_router)
app.include_router(excercise_router)
app.include_router(exerciseEntry_router)


Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite solicitudes de estos dominios
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras (headers)
)


@app.get('/', tags=['home']) #tags es para poder clasificar los endpoints y facilita su busqueda
def message():
    return HTMLResponse('<h1>Hola Gym buddy :)</h1>')