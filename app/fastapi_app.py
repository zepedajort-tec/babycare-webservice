import bcrypt
from fastapi import FastAPI, HTTPException, Depends
from app import crud_babies
from app import crud_parents
from app import crud_records
from auth_utils import create_access_token
from auth_dependency import get_current_user
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
app = FastAPI(title="BabyCare API (FastAPI)", version="1.2")

# =======================
# LOGIN & REGISTRO (NO requieren JWT)
# =======================

@app.post("/login")
def login_parent(data: dict):
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
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
    return {"access_token": token, "token_type": "bearer"}

@app.post("/register")
def register_parent(parent: dict):
    required_fields = ["name", "email", "password"]
    for field in required_fields:
        if field not in parent or not parent[field]:
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
        parent.get("sex", "O"),
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

# =======================
# ENDPOINTS TABLA BABY_PROFILES
# =======================

@app.get("/babies")
def get_babies(user=Depends(get_current_user)):
    return crud_babies.get_all_babies()

@app.get("/babies/{baby_id}")
def get_baby(baby_id: int, user=Depends(get_current_user)):
    result = crud_babies.get_baby_by_id(baby_id)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Baby not found")
    return result

@app.post("/babies")
def create_baby(baby: dict, user=Depends(get_current_user)):
    try:
        return crud_babies.create_baby(
            baby["parent_id"],
            baby["name"],
            baby["age_months"],
            baby.get("weight", None),
            baby.get("height", None)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/babies/{baby_id}")
def update_baby(baby_id: int, baby: dict, user=Depends(get_current_user)):
    return crud_babies.update_baby(
        baby_id,
        baby["parent_id"],
        baby["name"],
        baby["age_months"],
        baby.get("weight", None),
        baby.get("height", None)
    )

@app.delete("/babies/{baby_id}")
def delete_baby(baby_id: int, user=Depends(get_current_user)):
    return crud_babies.delete_baby(baby_id)

# =======================
# ENDPOINTS TABLA PARENTS
# =======================

@app.get("/parents")
def get_parents(user=Depends(get_current_user)):
    return crud_parents.get_all_parents()

@app.get("/parents/{parent_id}")
def get_parent(parent_id: int, user=Depends(get_current_user)):
    result = crud_parents.get_parent_by_id(parent_id)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Parent not found")
    return result

@app.put("/parents/{parent_id}")
def update_parent(parent_id: int, parent: dict, user=Depends(get_current_user)):
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
    return crud_parents.delete_parent(parent_id)

# =======================
# ENDPOINTS TABLA HEALTH_RECORDS
# =======================

@app.get("/records")
def get_records(user=Depends(get_current_user)):
    return crud_records.get_all_records()

@app.get("/records/{record_id}")
def get_record(record_id: int, user=Depends(get_current_user)):
    result = crud_records.get_record_by_id(record_id)
    if not result or "message" in result:
        raise HTTPException(status_code=404, detail="Record not found")
    return result

@app.post("/records")
def create_record(record: dict, user=Depends(get_current_user)):
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
    return crud_records.update_record(
        record_id,
        record["baby_id"],
        record["date"],
        record["vaccine"],
        record.get("notes", None)
    )

@app.delete("/records/{record_id}")
def delete_record(record_id: int, user=Depends(get_current_user)):
    return crud_records.delete_record(record_id)