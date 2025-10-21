from sqlalchemy.orm import Session
from webservice.models import baby_profile as model
from webservice.schemas import baby_profile_schemas as schema


# --- BabyProfile ---
def create_baby(db: Session, baby: schema.BabyProfileCreate):
    db_baby = model.BabyProfile(**baby.dict())
    db.add(db_baby)
    db.commit()
    db.refresh(db_baby)
    return db_baby


def get_babies(db: Session):
    return db.query(model.BabyProfile).all()


def get_baby(db: Session, baby_id: int):
    return db.query(model.BabyProfile).filter(
        model.BabyProfile.id == baby_id
    ).first()


def update_baby(db: Session, baby_id: int, baby: schema.BabyProfileCreate):
    db_baby = get_baby(db, baby_id)
    if db_baby:
        for key, value in baby.dict().items():
            setattr(db_baby, key, value)
        db.commit()
        db.refresh(db_baby)
    return db_baby


def delete_baby(db: Session, baby_id: int):
    db_baby = get_baby(db, baby_id)
    if db_baby:
        db.delete(db_baby)
        db.commit()
