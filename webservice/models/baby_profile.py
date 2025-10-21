from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from webservice.db.database import Base

class BabyProfile(Base):
    __tablename__ = "baby_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age_months = Column(Integer)
    weight = Column(Float)
    height = Column(Float)

    health_records = relationship("HealthRecord", back_populates="baby")