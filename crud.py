from sqlalchemy.orm import Session
import models
import pydantic_models
from fastapi import HTTPException


def get_auto(db: Session, auto_id: int):
    db_auto = db.query(models.Auto).filter(models.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_auto


def get_autos(db: Session, skip: int = 0, limit: int = 100):
    db_autos = db.query(models.Auto).offset(skip).limit(limit).all()
    if db_autos is None or db_autos == [ ]:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_autos


def create_auto(db: Session, auto: pydantic_models.AutoBase):
    db_auto = models.Auto(brand=auto.brand, age=auto.age, cost=auto.cost, mileage=auto.mileage, is_sell=auto.is_sell)
    db.add(db_auto)
    db.commit()
    db.refresh(db_auto)
    return db_auto


def delete_auto(db: Session, auto_id: int):
    db_auto = db.query(models.Auto).filter(models.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_auto)
    db.commit()
    return {"delete": True}


def update_auto(db: Session, auto_id: int, auto: pydantic_models.AutoBase):
    db_auto = db.query(models.Auto).filter(models.Auto.id == auto_id).first()
    if db_auto is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_auto.brand = auto.brand
    db_auto.age = auto.age
    db_auto.cost = auto.cost
    db_auto.mileage = auto.mileage
    db_auto.is_sell = auto.is_sell
    db.commit()
    return db_auto



