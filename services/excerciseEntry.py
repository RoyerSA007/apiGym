from fastapi import HTTPException
from typing import List




from models.user import User as UserModel
from schemas.user import User

from models.exercises import Ejercicio as EjercicioModel
from schemas.exercises import Ejercicio

from models.exerciseEntries import EntradaEjercicio as EntradaEjercicioModel
from schemas.excerciseEntry import ExerciseEntry

class ExcerciseEntryService():
    def __init__(self, db) -> None:
            self.db = db

    def get_entradasEjercicio(self):
        result = self.db.query(EntradaEjercicioModel).all()
        return result
    
    def get_entradaEjercicio(self, id_en: int):
        result =  self.db.query(EntradaEjercicioModel).filter(EntradaEjercicioModel.id_en == id_en).first()
        return result
    
    def create_entradaEjercicio(self, entrada: ExerciseEntry):
        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == entrada.user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar si el ejercicio existe
        exercise_exists = self.db.query(EjercicioModel).filter(EjercicioModel.id_ex == entrada.exercise_id).first()
        if exercise_exists is None:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        # Crear la nueva entrada si ambos existen
        new_Entrada = EntradaEjercicioModel(**entrada.model_dump())
        self.db.add(new_Entrada)
        self.db.commit()
        
        return new_Entrada 
    
    def get_weights_by_user_and_exercise(self, user_id: int, exercise_id: int) -> List[float]:

        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar si el ejercicio existe
        exercise_exists = self.db.query(EjercicioModel).filter(EjercicioModel.id_ex == exercise_id).first()
        if exercise_exists is None:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        # Obtener solo los pesos registrados para el usuario y el ejercicio
        results = (
            self.db.query(EntradaEjercicioModel.weight)
            .filter(
                EntradaEjercicioModel.user_id == user_id, 
                EntradaEjercicioModel.exercise_id == exercise_id
            )
            .with_entities(EntradaEjercicioModel.weight)
            .all()
        )


        # Extraer los valores de peso de las filas devueltas
        weights = [row[0] for row in results]


        return weights


    
    def get_reps_by_user_and_exercise(self, user_id: int, exercise_id: int) -> List[float]:
        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar si el ejercicio existe
        exercise_exists = self.db.query(EjercicioModel).filter(EjercicioModel.id_ex == exercise_id).first()
        if exercise_exists is None:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        # Obtener todos los pesos registrados para el usuario y el ejercicio
        reps = (
            self.db.query(EntradaEjercicioModel.reps)
            .filter(EntradaEjercicioModel.user_id == user_id, EntradaEjercicioModel.exercise_id == exercise_id)
            .all()
        )

        repsTotal=[rep[0] for rep in reps] 

        # Extraer los pesos de los resultados
        return repsTotal
    
    def get_entries_by_user(self, user_id: int) -> List[EntradaEjercicioModel]:
        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Obtener todas las entradas de ejercicio del usuario
        entries = self.db.query(EntradaEjercicioModel).filter(EntradaEjercicioModel.user_id == user_id).all()

        return entries
    
    def get_weights_by_user_and_exercise_graph(self, user_id: int, exercise_id: int) -> List[tuple]:
        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar si el ejercicio existe
        exercise_exists = self.db.query(EjercicioModel).filter(EjercicioModel.id_ex == exercise_id).first()
        if exercise_exists is None:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        # Obtener todos los pesos y fechas registrados para el usuario y el ejercicio
        entries = (
            self.db.query(EntradaEjercicioModel.weight, EntradaEjercicioModel.date)
            .filter(EntradaEjercicioModel.user_id == user_id, EntradaEjercicioModel.exercise_id == exercise_id)
            .all()
        )

        return entries 
    
    def get_all_entries_by_user(self, user_id: int) -> List[EntradaEjercicioModel]:
        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Obtener todas las entradas de ejercicio del usuario
        entries = self.db.query(EntradaEjercicioModel).filter(EntradaEjercicioModel.user_id == user_id).all()

        return entries
    
    def get_reps_by_user_and_exercise_graph(self, user_id: int, exercise_id: int) -> List[tuple]:
        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar si el ejercicio existe
        exercise_exists = self.db.query(EjercicioModel).filter(EjercicioModel.id_ex == exercise_id).first()
        if exercise_exists is None:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        # Obtener todos los pesos y fechas registrados para el usuario y el ejercicio
        entries = (
            self.db.query(EntradaEjercicioModel.reps, EntradaEjercicioModel.date)
            .filter(EntradaEjercicioModel.user_id == user_id, EntradaEjercicioModel.exercise_id == exercise_id)
            .all()
        )

        return entries 
    
    def get_excercises_by_user(self, user_id: int) -> List[dict]:
        # Verificar si el usuario existe
        user_exists = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_exists is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Obtener todas las entradas de ejercicio del usuario con exercise_id, peso y repeticiones
        entries = (
            self.db.query(
                EntradaEjercicioModel.exercise_id,
                EntradaEjercicioModel.weight,
                EntradaEjercicioModel.reps,
                EjercicioModel.nombre,
                EntradaEjercicioModel.date,
                UserModel.name
            )

            .join(EjercicioModel, EjercicioModel.id_ex == EntradaEjercicioModel.exercise_id)
            .filter(EntradaEjercicioModel.user_id == user_id)
            .all()
        )
        
        if not entries:
            raise HTTPException(status_code=404, detail="No se encontraron entradas de ejercicio para el usuario")

        # Formatear el resultado como una lista de diccionarios, que incluye el nombre del ejercicio, peso y repeticiones
        results = [
            {
                "nombreUser":entry.name,
                "nombre": entry.nombre,
                "peso": entry.weight,
                "reps": entry.reps,
                "fecha": entry.date
            }
            for entry in entries
        ]
        
        return results