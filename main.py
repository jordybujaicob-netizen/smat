from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="SMAT API - Sistema de Monitoreo")

# --- MODELOS DE DATOS ---

class Estacion(BaseModel):
    id: int
    nombre: str
    ubicacion: str

class Lectura(BaseModel):
    estacion_id: int
    valor: float

# --- BASES DE DATOS VOLÁTILES (LISTAS) ---

db_estaciones = []
db_lecturas = []

# --- ENDPOINTS DE ESTACIONES ---

@app.post("/estaciones/", status_code=201)
async def crear_estacion(estacion: Estacion):
    """Crea una nueva estación de monitoreo"""
    db_estaciones.append(estacion)
    return {"msj": "Estación creada", "data": estacion}

@app.get("/estaciones/", response_model=List[Estacion])
async def listar_estaciones():
    """Lista todas las estaciones registradas"""
    return db_estaciones

# --- ENDPOINTS DE LECTURAS ---

@app.post("/lecturas/", status_code=201)
async def registrar_lectura(lectura: Lectura):
    """Registra una nueva lectura de un sensor"""
    db_lecturas.append(lectura)
    return {"status": "Lectura recibida"}

# --- MOTOR DE RIESGO Y HISTORIAL ---

@app.get("/estaciones/{id}/riesgo")
async def obtener_riesgo(id: int):
    """Calcula el riesgo basado en la última lectura"""
    # 1. Verificar si la estación existe
    estacion_existe = any(e.id == id for e in db_estaciones)
    if not estacion_existe:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    # 2. Filtrar lecturas por ID
    lecturas = [l.valor for l in db_lecturas if l.estacion_id == id]
    if not lecturas:
        return {"id": id, "nivel": "SIN DATOS", "valor": 0}

    # 3. Lógica del motor de reglas
    ultima_lectura = lecturas[-1]
    if ultima_lectura > 20.0:
        nivel = "PELIGRO"
    elif ultima_lectura > 10.0:
        nivel = "ALERTA"
    else:
        nivel = "NORMAL"
    
    return {"id": id, "valor": ultima_lectura, "nivel": nivel}

@app.get("/estaciones/{id}/historial")
async def obtener_historial(id: int):
    """Implementación del Reto: Devuelve historial y promedio de lecturas"""
    # 1. Validación de existencia
    estacion_existe = any(e.id == id for e in db_estaciones)
    if not estacion_existe:
        raise HTTPException(status_code=404, detail="Estación no encontrada")
    
    # 2. Filtrar lecturas asociadas
    lecturas_estacion = [l.valor for l in db_lecturas if l.estacion_id == id]
    
    # 3. Cálculos matemáticos
    conteo = len(lecturas_estacion)
    promedio = sum(lecturas_estacion) / conteo if conteo > 0 else 0.0
    
    return {
        "estacion_id": id,
        "lecturas": lecturas_estacion,
        "conteo": conteo,
        "promedio": round(promedio, 2)
    }
