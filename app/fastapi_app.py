import bcrypt
from fastapi import FastAPI, HTTPException, Depends
from app import crud_babies
from app import crud_parents
from app import crud_records
from app import crud_development_tips as crud_devtips
from app.auth_utils import create_access_token, verify_jwt_token
from app.auth_dependency import get_current_user
from fastapi.security import OAuth2PasswordBearer

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="BabyCare API (FastAPI)", version="1.3")

# =======================
# LOGIN & REGISTRO (NO requieren JWT)
# =======================

@app.post("/login")
def login_parent(data: dict):
    email = data.get("email")
    password = data.get("password")
    if not email or not password or email == "" or password == "":
        raise HTTPException(status_code=400, detail="Email and password are required")

    parent = crud_parents.get_parent_by_email(email)
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    password_hash = parent['password_hash'] if isinstance(parent, dict) else parent[7]
    if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token_data = {
        "user_id": parent['id'] if isinstance(parent, dict) else parent[0],
        "email": email,
        "name": parent['name'] if isinstance(parent, dict) else parent[1]
    }
    token = create_access_token(token_data)
    return {"access_token": token, "parent": "bearer"}

@app.post("/register")
def register_parent(parent: dict):
    required_fields = ["name", "email", "password"]
    for field in required_fields:
        if field not in parent or not parent[field] or parent[field] == "":
            raise HTTPException(status_code=400, detail=f"Field {field} is required")
    existing = crud_parents.get_parent_by_email(parent["email"])
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")
    password_hash = bcrypt.hashpw(parent["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    crud_parents.create_parent(
        parent["name"],
        parent["email"],
        parent.get("phone", None),
        parent.get("relation", None),
        parent.get("age", None),
        password_hash
    )
    saved_parent = crud_parents.get_parent_by_email(parent["email"])
    token_data = {
        "user_id": saved_parent["id"] if isinstance(saved_parent, dict) else saved_parent[0],
        "email": saved_parent["email"] if isinstance(saved_parent, dict) else saved_parent[2],
        "name": saved_parent["name"] if isinstance(saved_parent, dict) else saved_parent[1]
    }
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/refresh-token")
def refresh_token(token: str = Depends(oauth2_scheme)):
    if not token or token == "":
        raise HTTPException(status_code=400, detail="Token is required")
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    new_token = create_access_token({
        "user_id": payload["user_id"],
        "email": payload["email"],
        "name": payload["name"]
    })
    return {"access_token": new_token, "token_type": "bearer"}

# =======================
# ENDPOINTS TABLA BABY_PROFILES
# =======================

@app.get("/babies")
def get_babies(user=Depends(get_current_user)):
    return crud_babies.get_all_babies()

@app.get("/babies/{baby_id}")
def get_baby(baby_id: int, user=Depends(get_current_user)):
    if baby_id is None:
        raise HTTPException(status_code=400, detail="baby_id is required")
    result = crud_babies.get_baby_by_id(baby_id)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Baby not found")
    return result

@app.get("/parents/{parent_id}/babies")
def get_babies_by_parent(parent_id: int, user=Depends(get_current_user)):
    if parent_id is None:
        raise HTTPException(status_code=400, detail="parent_id is required")

    result = crud_babies.get_babies_by_parent_id(parent_id)

    # Normalizar: si el CRUD devuelve None -> respondemos [] con 200 OK
    if result is None:
        return []

    # Si devuelve una lista (incluso vacía) -> devolvemos tal cual
    if isinstance(result, list):
        return result

    # Si devuelve dict con 'message' -> error (404)
    if isinstance(result, dict) and "message" in result:
        raise HTTPException(status_code=404, detail=result.get("message", "Baby not found"))

    # En cualquier otro caso devolvemos result (por compatibilidad)
    return result

@app.post("/babies")
def create_baby(baby: dict, user=Depends(get_current_user)):
    required_fields = ["parent_id", "name", "age_months", "sex"]
    for field in required_fields:
        if field not in baby or baby[field] is None or baby[field] == "":
            raise HTTPException(status_code=400, detail=f"Field {field} is required.")
    try:
        created = crud_babies.create_baby(
            baby["parent_id"],
            baby["name"],
            baby["age_months"],
            baby.get("sex", "O"),
            baby.get("weight", None),
            baby.get("height", None)
        )
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.put("/babies/{baby_id}")
def update_baby(baby_id: int, baby: dict, user=Depends(get_current_user)):
    if baby_id is None:
        raise HTTPException(status_code=400, detail="baby_id is required")
    required_fields = ["parent_id", "name", "age_months", "sex"]
    for field in required_fields:
        if field not in baby or baby[field] is None or baby[field] == "":
            raise HTTPException(status_code=400, detail=f"Field {field} is required.")
    return crud_babies.update_baby(
        baby_id,
        baby["parent_id"],
        baby["name"],
        baby["age_months"],
        baby.get("sex", "O"),
        baby.get("weight", None),
        baby.get("height", None)
    )

@app.delete("/babies/{baby_id}")
def delete_baby(baby_id: int, user=Depends(get_current_user)):
    if baby_id is None:
        raise HTTPException(status_code=400, detail="baby_id is required")
    return crud_babies.delete_baby(baby_id)

# =======================
# ENDPOINTS TABLA PARENTS
# =======================

@app.get("/parents")
def get_parents(user=Depends(get_current_user)):
    return crud_parents.get_all_parents()

@app.get("/parent/{email}")
def get_parent_by_email(email: str, user=Depends(get_current_user)):
    if not email or email == "":
        raise HTTPException(status_code=400, detail="Email is required")
    result = crud_parents.get_parent_by_email(email)
    if not result:
        raise HTTPException(status_code=404, detail="Parent not found")
    # Nota: elimina password_hash del resultado por seguridad antes de retornar
    if isinstance(result, dict):
        result.pop("password_hash", None)
    elif isinstance(result, (list, tuple)) and len(result) > 7:
        result = result[:7]  # solo deja id, name, email, phone, relation, age, sex
    return result

@app.get("/parents/{parent_id}")
def get_parent(parent_id: int, user=Depends(get_current_user)):
    if parent_id is None:
        raise HTTPException(status_code=400, detail="parent_id is required")
    result = crud_parents.get_parent_by_id(parent_id)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Parent not found")
    return result

@app.put("/parents/{parent_id}")
def update_parent(parent_id: int, parent: dict, user=Depends(get_current_user)):
    if parent_id is None:
        raise HTTPException(status_code=400, detail="parent_id is required")
    required_fields = ["name", "email", "password_hash"]
    for field in required_fields:
        if field not in parent or parent[field] is None or parent[field] == "":
            raise HTTPException(status_code=400, detail=f"Field {field} is required.")
    return crud_parents.update_parent(
        parent_id,
        parent["name"],
        parent["email"],
        parent.get("phone", None),
        parent.get("relation", None),
        parent.get("age", None),
        parent.get("sex", "O"),
        parent["password_hash"]
    )

@app.delete("/parents/{parent_id}")
def delete_parent(parent_id: int, user=Depends(get_current_user)):
    if parent_id is None:
        raise HTTPException(status_code=400, detail="parent_id is required")
    return crud_parents.delete_parent(parent_id)

# =======================
# ENDPOINTS TABLA HEALTH_RECORDS
# =======================

@app.get("/records")
def get_records(user=Depends(get_current_user)):
    return crud_records.get_all_records()

@app.get("/records/{record_id}")
def get_record(record_id: int, user=Depends(get_current_user)):
    if record_id is None:
        raise HTTPException(status_code=400, detail="record_id is required")
    result = crud_records.get_record_by_id(record_id)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Record not found")
    return result

@app.post("/records")
def create_record(record: dict, user=Depends(get_current_user)):
    required_fields = ["baby_id", "date", "vaccine"]
    for field in required_fields:
        if field not in record or record[field] is None or record[field] == "":
            raise HTTPException(status_code=400, detail=f"Field {field} is required.")
    try:
        return crud_records.create_record(
            record["baby_id"],
            record["date"],
            record["vaccine"],
            record.get("notes", None)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/records/{record_id}")
def update_record(record_id: int, record: dict, user=Depends(get_current_user)):
    if record_id is None:
        raise HTTPException(status_code=400, detail="record_id is required")
    required_fields = ["baby_id", "date", "vaccine"]
    for field in required_fields:
        if field not in record or record[field] is None or record[field] == "":
            raise HTTPException(status_code=400, detail=f"Field {field} is required.")
    return crud_records.update_record(
        record_id,
        record["baby_id"],
        record["date"],
        record["vaccine"],
        record.get("notes", None)
    )

@app.delete("/records/{record_id}")
def delete_record(record_id: int, user=Depends(get_current_user)):
    if record_id is None:
        raise HTTPException(status_code=400, detail="record_id is required")
    return crud_records.delete_record(record_id)
    
# =======================
# ENDPOINTS TABLA DEVELOPMENT_TIPS (DevTips)
# =======================

@app.get("/devtips")
def get_devtips(user=Depends(get_current_user)):
    """Obtiene todos los consejos de desarrollo"""
    try:
        tips = crud_devtips.get_all_devtips()
        if not tips:
            return []
        return tips
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devtips/{tip_id}")
def get_devtip(tip_id: int, user=Depends(get_current_user)):
    """Obtiene un consejo específico por su ID"""
    if not tip_id:
        raise HTTPException(status_code=400, detail="tip_id is required")
    try:
        tip = crud_devtips.get_devtip_by_id(tip_id)
        if not tip or "message" in tip:
            raise HTTPException(status_code=404, detail="DevTip not found")
        return tip
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devtips")
def create_devtip(tip: dict, user=Depends(get_current_user)):
    """Crea un nuevo consejo de desarrollo"""
    required_fields = ["title", "description", "age_min", "age_max", "category"]
    for field in required_fields:
        if field not in tip or tip[field] in (None, ""):
            raise HTTPException(status_code=400, detail=f"Field {field} is required")

    try:
        crud_devtips.create_devtip(
            tip["title"],
            tip["description"],
            tip["age_min"],
            tip["age_max"],
            tip["category"]
        )
        return {"message": "Development Tip created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/devtips/{tip_id}")
def update_devtip(tip_id: int, tip: dict, user=Depends(get_current_user)):
    """Actualiza un consejo existente"""
    if not tip_id:
        raise HTTPException(status_code=400, detail="tip_id is required")

    required_fields = ["title", "description", "age_min", "age_max", "category"]
    for field in required_fields:
        if field not in tip or tip[field] in (None, ""):
            raise HTTPException(status_code=400, detail=f"Field {field} is required")

    try:
        crud_devtips.update_devtip(
            tip_id,
            tip["title"],
            tip["description"],
            tip["age_min"],
            tip["age_max"],
            tip["category"]
        )
        return {"message": "Development Tip updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/devtips/{tip_id}")
def delete_devtip(tip_id: int, user=Depends(get_current_user)):
    """Elimina un consejo por ID"""
    if not tip_id:
        raise HTTPException(status_code=400, detail="tip_id is required")
    try:
        crud_devtips.delete_devtip(tip_id)
        return {"message": "Development Tip deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




