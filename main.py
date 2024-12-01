from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from routers.user import user_router
from routers.exercise import excercise_router
from routers.excerciseEntry import exerciseEntry_router


from models.user import User  # Asegúrate de importar todos los modelos
from models.exercises import Ejercicio
from models.exerciseEntries import EntradaEjercicio


# from middlewares.error_handler import ErrorHandler




app = FastAPI()
app.title = "Gym Buddy"
app.version = "0.0.1"

app.include_router(user_router)
app.include_router(excercise_router)
app.include_router(exerciseEntry_router)


Base.metadata.create_all(bind=engine)


@app.get('/', tags=['home']) #tags es para poder clasificar los endpoints y facilita su busqueda
def message():
    return HTMLResponse('<h1>Hola Gym buddy :)</h1>')
