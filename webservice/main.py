from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, models
from db import SessionLocal, engine

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="BabyCare Backend API", version="1.0")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- BabyProfile CRUD ---
@app.post("/babies/", response_model=schemas.BabyProfile)
def create_baby(baby: schemas.BabyProfileCreate, db: Session = Depends(get_db)):
    return crud.create_baby(db=db, baby=baby)

@app.get("/babies/", response_model=list[schemas.BabyProfile])
def get_babies(db: Session = Depends(get_db)):
    return crud.get_babies(db=db)

@app.get("/babies/{baby_id}", response_model=schemas.BabyProfile)
def get_baby(baby_id: int, db: Session = Depends(get_db)):
    db_baby = crud.get_baby(db, baby_id)
    if not db_baby:
        raise HTTPException(status_code=404, detail="Baby not found")
    return db_baby

@app.put("/babies/{baby_id}", response_model=schemas.BabyProfile)
def update_baby(baby_id: int, baby: schemas.BabyProfileCreate, db: Session = Depends(get_db)):
    return crud.update_baby(db, baby_id, baby)

@app.delete("/babies/{baby_id}")
def delete_baby(baby_id: int, db: Session = Depends(get_db)):
    crud.delete_baby(db, baby_id)
    return {"message": "Baby deleted successfully"}
