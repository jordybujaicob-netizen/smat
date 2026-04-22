from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

def get_dashboard_stats(db: Session):

    total_estaciones = db.query(models.Estacion).count()

    total_lecturas = db.query(models.Lectura).count()

    punto_maximo = db.query(func.max(models.Lectura.valor)).scalar() or 0

    return {
        "total_estaciones": total_estaciones,
        "total_lecturas": total_lecturas,
        "punto_critico_maximo": punto_maximo
    }
