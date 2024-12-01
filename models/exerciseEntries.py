from config.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from models.user import User
from models.exercises import Ejercicio  



class EntradaEjercicio(Base):

    __tablename__="exerciseEntry"

    id_en = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    exercise_id = Column(Integer, ForeignKey('exercises.id_ex', ondelete='CASCADE'))     
    weight = Column(Float)
    reps = Column(Integer)
    date = Column(Date)

    # Relaciones para navegar entre tablas
    user = relationship("User", back_populates="exercise_entries")
    exercise = relationship("Ejercicio", back_populates="exercise_entries")
    