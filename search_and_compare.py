from sqlalchemy.orm import Session
import models
import pydantic_models
from fastapi import HTTPException


def compare_auto(db: Session, auto_id_1: int, auto_id_2: int):
    db_auto_1 = db.query(models.Auto).filter(models.Auto.id == auto_id_1).first()
    db_auto_2 = db.query(models.Auto).filter(models.Auto.id == auto_id_2).first()
    if db_auto_1 is None:
        raise HTTPException(status_code=404, detail="Item 1 not found")
    if db_auto_2 is None:
        raise HTTPException(status_code=404, detail="Item 2 not found")
    compare_result = {"car_1": db_auto_1, "car_2": db_auto_2, "newer_car": None, "how_newer":None, "cheaper_car": None, "how_cheaper": None}
    if db_auto_1.age > db_auto_2.age:
        compare_result["newer_car"] = db_auto_2
        compare_result["how_newer"] = db_auto_1.age - db_auto_2.age
    elif db_auto_1.age < db_auto_2.age:
        compare_result["newer_car"] = db_auto_1
        compare_result["how_newer"] = db_auto_2.age - db_auto_1.age
    else:
        compare_result["newer_car"] = None
        compare_result["how_newer"] = 0

    if db_auto_1.cost > db_auto_2.cost:
        compare_result["cheaper_car"] = db_auto_2
        compare_result["how_cheaper"] = db_auto_1.cost - db_auto_2.cost
    elif db_auto_1.cost < db_auto_2.cost:
        compare_result["cheaper_car"] = db_auto_1
        compare_result["how_cheaper"] = db_auto_2.cost - db_auto_1.cost
    else:
        compare_result["cheaper_car"] = None
        compare_result["how_cheaper"] = 0

    return compare_result


def filter_autos(db: Session, brand: str, cost_min, cost_max, age_min, age_max: int):
    print(cost_min, cost_max, age_min, age_max)
    db_autos = db.query(models.Auto).filter(models.Auto.brand.contains(brand), models.Auto.age >= age_min, models.Auto.age <= age_max,
                                            models.Auto.cost >= cost_min, models.Auto.cost <= cost_max).all()
    if db_autos is None or db_autos == []:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_autos
