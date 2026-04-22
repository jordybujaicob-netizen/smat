from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models

from .routers import reportes, infraestructura, reportes_viejos

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT Backend Profesional",
    description="API robusta para la gestión y monitoreo de desastres naturales.",
    version="1.0.1"
)

origins = ["*"] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Inicio"], summary="Bienvenida al Sistema")
def read_root():
    return {
        "status": "online",
        "message": "SMAT Backend Profesional Funcionando",
        "version": "1.0.1"
    }

app.include_router(infraestructura.router)
app.include_router(reportes.router)
app.include_router(reportes_viejos.router)
