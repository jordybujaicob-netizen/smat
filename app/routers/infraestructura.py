from fastapi import APIRouter

router = APIRouter(prefix="/tramos", tags=["Infraestructura"])

@router.get("/", summary="Listar tramos")
def listar_tramos():
    return {"mensaje": "Lista de tramos recuperada"}
