from sqlalchemy import Boolean, Column, Integer, String, Float

from database import Base


class Auto(Base):
    __tablename__ = "autos"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String)
    age = Column(Integer)
    cost = Column(Float)
    mileage = Column(String)
    is_sell = Column(Boolean, default=True)


