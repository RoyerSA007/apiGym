from pydantic import BaseModel, Field
from typing import Optional

class Ejercicio(BaseModel):
    id_ex: Optional[int] = None
    nombre: str = Field(min_length=2, max_length=55)


    class Config:
        json_schema_extra = {
            "example:":{
                "id_ex": 1,
                "nombre": "Sentadilla"
            }
        }