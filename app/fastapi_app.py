from fastapi import FastAPI, HTTPException
from app import crud_babies

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
