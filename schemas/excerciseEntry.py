from pydantic import BaseModel, Field
from typing import Optional
import datetime


class ExerciseEntry(BaseModel):
    id_en: Optional[int] = None
    user_id: Optional[int] = None
    exercise_id: Optional[int] = None
    weight: float = Field(ge=0, le=1000)
    reps: int = Field(ge=0, le=100)
    date: datetime.date = Field(..., description="La fecha en la que se realizó el ejercicio")  # Usando Field


    class Config:
        json_schema_extra = {
            "example": {  # Corregido el nombre de la clave
                "id_en": 1,
                "user_id": 2,
                "exercise_id": 1,
                "weight": 75.0,
                "reps": 10,
                "date": "2024-10-20"  # Ejemplo de fecha en formato ISO
            }
        }