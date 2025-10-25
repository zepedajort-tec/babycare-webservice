from fastapi import FastAPI, HTTPException
from app import crud_babies
from app import crud_parents
from app import crud_records
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
app = FastAPI(title="BabyCare API (FastAPI)", version="1.1")


@app.get("/babies")
def get_babies():
    return crud_babies.get_all_babies()


@app.get("/babies/{baby_id}")
def get_baby(baby_id: int):
    result = crud_babies.get_baby_by_id(baby_id)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Baby not found")
    return result


@app.post("/babies")
def create_baby(baby: dict):
    try:
        return crud_babies.create_baby(
            baby["name"],
            baby["age_months"],
            baby["weight"],
            baby["height"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/babies/{baby_id}")
def update_baby(baby_id: int, baby: dict):
    return crud_babies.update_baby(
        baby_id, baby["name"],
        baby["age_months"],
        baby["weight"],
        baby["height"]
    )


@app.delete("/babies/{baby_id}")
def delete_baby(baby_id: int):
    return crud_babies.delete_baby(baby_id)

# ==========================================================
# RUTAS PARA LA ENTIDAD 'PARENTS'
# ==========================================================

@app.get("/parents")
def get_parents():
    """Obtiene todos los padres/madres."""
    return crud_parents.get_all_parents()


@app.get("/parents/{parent_id}")
def get_parent(parent_id: int):
    """Consulta un padre/madre por ID."""
    result = crud_parents.get_parent_by_id(parent_id)
    # Reutilizamos el manejo de error 404 (Not Found)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Parent not found")
    return result


@app.post("/parents")
def create_parent(parent: dict):
    """Crea un nuevo padre/madre. Se asume que incluye el campo 'relation'."""
    try:
        return crud_parents.create_parent(
            parent["name"],
            parent["email"],
            parent["phone"],
            parent["relation"]  # Incluye el nuevo campo 'relation'
        )
    except Exception as e:
        # En caso de errores en la base de datos o campos faltantes
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/parents/{parent_id}")
def update_parent(parent_id: int, parent: dict):
    """Actualiza un padre/madre existente. Se asume que incluye 'relation'."""
    return crud_parents.update_parent(
        parent_id,
        parent["name"],
        parent["email"],
        parent["phone"],
        parent["relation"]  # Incluye el nuevo campo 'relation'
    )


@app.delete("/parents/{parent_id}")
def delete_parent(parent_id: int):
    """Elimina un padre/madre por ID."""
    return crud_parents.delete_parent(parent_id)

# ==========================================================
# RUTAS PARA LA ENTIDAD 'RECORDS'
# ==========================================================

@app.get("/records")
def get_records():
    """Obtiene todos los estados."""
    return crud_records.get_all_records()


@app.get("/records/{record_id}")
def get_record(record_id: int):
    """Consulta un estado por ID."""
    result = crud_records.get_record_by_id(record_id)
    # Reutilizamos el manejo de error 404 (Not Found)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Record not found")
    return result


@app.post("/records")
def create_record(record: dict):
    """Crea un nuevo estado. Se asume que incluye el campo 'relation'."""
    try:
        return crud_records.create_record(
            record["babyid"],
            record["date"],
            record["vaccine"],
            record["notes"]  # Incluye el nuevo campo 'relation'
        )
    except Exception as e:
        # En caso de errores en la base de datos o campos faltantes
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/records/{record_id}")
def update_record(record_id: int, record: dict):
    """Actualiza un record existente. Se asume que incluye 'relation'."""
    return crud_records.update_record(
        record_id,
        parent["babyid"],
        parent["date"],
        parent["vaccine"],
        parent["notes"]  # Incluye el nuevo campo 'relation'
    )


@app.delete("/records/{record_id}")
def delete_parent(record: int):
    """Elimina el estado por ID."""
    return crud_records.delete_record(record_id)
