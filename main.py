from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    description="""
API robusta para la gestión y monitoreo de desastres naturales.
Permite la telemetría de sensores en tiempo real y el cálculo de niveles de riesgo.

**Entidades principales:**
* **Estaciones:** Puntos de monitoreo físico.
* **Lecturas:** Datos capturados por sensores.
* **Riesgos:** Análisis de niveles de alerta.
""",
    version="1.0.1",
    contact={
        "name": "Soporte Técnico SMAT",
        "email": "soporte.smat@unmsm.edu.pe",
    }
)


@app.get("/", tags=["Inicio"], summary="Bienvenida")
def read_root():
    return {"mensaje": "API SMAT Funcionando"}

@app.get("/tramos", 
         tags=["Infraestructura"], 
         summary="Listar tramos", 
         description="Retorna la lista completa de tramos registrados.")
def obtener_tramos():
    return {"tramos": ["Tramo A", "Tramo B"]}

@app.get("/estaciones/{id}/historial", 
         tags=["Reportes Históricos"], 
         summary="Historial estadístico", 
         description="Calcula el conteo y promedio de lecturas para una estación específica.",
         responses={404: {"description": "Estación no encontrada"}})
def obtener_historial(id: int):
    if id > 100:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    return {"estacion_id": id, "conteo": 10, "promedio": 25.4}

@app.get("/reportes/criticos", 
         tags=["Auditoria"], 
         summary="Reportes críticos", 
         description="Explica el funcionamiento del parámetro opcional umbral.")
def reportes_criticos(umbral: Optional[float] = 0.5):
    return {"umbral_aplicado": umbral, "estaciones": []}
