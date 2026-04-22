from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database, schemas

router = APIRouter(tags=["Reportes Históricos"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats", summary="Resumen Ejecutivo del Sistema")
def obtener_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)
