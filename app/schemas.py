from pydantic import BaseModel
from typing import Optional

class EstacionBase(BaseModel):
    nombre: str
    ubicacion: str

class EstacionCreate(EstacionBase):
    pass

class Estacion(EstacionBase):
    id: int

    class Config:
        from_attributes = True 
