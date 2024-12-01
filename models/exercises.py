from config.database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship



class Ejercicio(Base):

    __tablename__="exercises"

    id_ex = Column(Integer, primary_key = True)
    nombre = Column(String)
    

    exercise_entries = relationship("EntradaEjercicio", back_populates="exercise")
