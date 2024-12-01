from models.exercises import Ejercicio as EjercicioModel
from schemas.exercises import Ejercicio

class EjercicioService():
    def __init__(self, db) -> None:
            self.db = db

    def get_ejercicios(self):
        result = self.db.query(EjercicioModel).all()
        return result
    
    def get_ejercicio(self, id_ex: int):
        result =  self.db.query(EjercicioModel).filter(EjercicioModel.id_ex == id_ex).first()
        return result
    
    def create_ejercicio(self, ejercicio : Ejercicio):
        new_ejercicio =  EjercicioModel(**ejercicio.model_dump())
        self.db.add(new_ejercicio)
        self.db.commit()
        return 
    
    def delete_ejercicio(self, id_ex: int):
        result = self.db.query(EjercicioModel).filter(EjercicioModel.id_ex == id_ex).first()
        if not result:
            return {"message":"No existe el ejercicio"}
        self.db.delete(result)              
        self.db.commit()
        return {"message":"Ejercicio eliminado"}