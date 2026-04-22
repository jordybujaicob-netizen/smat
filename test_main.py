from fastapi.testclient import TestClient
from main import app

# Instanciamos el cliente de pruebas
client = TestClient(app)

def test_crear_estacion():
    """Prueba la fase 1: Creación de una estación"""
    response = client.post("/estaciones/", json={
        "id": 1,
        "nombre": "Estación Rimac",
        "ubicacion": "Chosica"
    })
    assert response.status_code == 201
    assert response.json()["data"]["nombre"] == "Estación Rimac"

def test_registrar_lectura():
    """Prueba la fase 2: Registro de una lectura"""
    # Primero aseguramos que la estación existe (las listas se reinician en cada ejecución de pytest)
    client.post("/estaciones/", json={"id": 1, "nombre": "Test", "ubicacion": "Test"})
    
    response = client.post("/lecturas/", json={
        "estacion_id": 1,
        "valor": 12.5
    })
    assert response.status_code == 201
    assert response.json()["status"] == "Lectura recibida"

def test_motor_riesgo_niveles():
    """Prueba la fase 3: Clasificación de riesgo"""
    client.post("/estaciones/", json={"id": 10, "nombre": "Misti", "ubicacion": "Arequipa"})
    
    # Caso Peligro (> 20.0)
    client.post("/lecturas/", json={"estacion_id": 10, "valor": 25.5})
    res_p = client.get("/estaciones/10/riesgo")
    assert res_p.json()["nivel"] == "PELIGRO"
    
    # Caso Alerta (> 10.0)
    client.post("/lecturas/", json={"id": 10, "estacion_id": 10, "valor": 15.0})
    res_a = client.get("/estaciones/10/riesgo")
    assert res_a.json()["nivel"] == "ALERTA"

def test_historial_y_promedio():
    """Prueba el Reto: Validación de historial, conteo y promedio"""
    # 1. Registro de estación para el reto
    client.post("/estaciones/", json={
        "id": 20, 
        "nombre": "Rio Yauli", 
        "ubicacion": "La Oroya"
    })
    
    # 2. Registro de 3 lecturas: 10.0, 20.0, 30.0 (Suma = 60.0, Promedio = 20.0)
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 10.0})
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 20.0})
    client.post("/lecturas/", json={"estacion_id": 20, "valor": 30.0})
    
    # 3. Validación del historial y promedio
    response = client.get("/estaciones/20/historial")
    assert response.status_code == 200
    
    data = response.json()
    assert data["estacion_id"] == 20
    assert len(data["lecturas"]) == 3
    assert data["conteo"] == 3
    assert data["promedio"] == 20.0

def test_estacion_no_encontrada():
    """Prueba la validación de error 404"""
    response = client.get("/estaciones/999/historial")
    assert response.status_code == 404
    assert response.json()["detail"] == "Estación no encontrada"
