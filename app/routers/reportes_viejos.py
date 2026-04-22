from fastapi import APIRouter

router = APIRouter()

@router.get("/estaciones/{id}/historial", tags=["Reportes Históricos"])
def historial(id: int):
    return {"estacion_id": id, "historial": "Datos recuperados"}

@router.get("/reportes/criticos", tags=["Auditoria"])
def reportes_criticos():
    return {"criticos": "Lista de reportes críticos"}
