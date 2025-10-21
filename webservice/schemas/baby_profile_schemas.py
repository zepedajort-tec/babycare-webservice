from pydantic import BaseModel

# --- BabyProfile ---
class BabyProfileBase(BaseModel):
    name: str
    age_months: int
    weight: float
    height: float

class BabyProfileCreate(BabyProfileBase):
    pass

class BabyProfile(BabyProfileBase):
    id: int
    class Config:
        orm_mode = True