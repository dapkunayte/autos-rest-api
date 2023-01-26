from fastapi import FastAPI, Depends
import crud, models, pydantic_models
import search_and_compare as sac
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/autos", response_model=list[pydantic_models.Auto])
def get_autos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    autos = crud.get_autos(db, skip=skip, limit=limit)
    return autos


@app.get("/autos/{auto_id}", response_model=pydantic_models.Auto)
def get_auto_by_id(auto_id: int, db: Session = Depends(get_db)):
    auto = crud.get_auto(db, auto_id=auto_id)
    return auto


@app.post("/autos", response_model=pydantic_models.AutoBase)
def create_auto(auto: pydantic_models.AutoBase, db: Session = Depends(get_db)):
    return crud.create_auto(db=db, auto=auto)


@app.delete("/autos/{auto_id}")
def delete_auto(auto_id: int, db: Session = Depends(get_db)):
    return crud.delete_auto(db=db, auto_id=auto_id)


@app.put("/autos/{auto_id}", response_model=pydantic_models.AutoBase)
def update(auto_id: int, auto: pydantic_models.AutoBase, db: Session = Depends(get_db)):
    return crud.update_auto(db=db, auto_id=auto_id, auto=auto)


@app.get("/autos/{auto_id_1}/{auto_id_2}")
def compare_autos(auto_id_1, auto_id_2: int, db: Session = Depends(get_db)):
    return sac.compare_auto(db=db, auto_id_1=auto_id_1, auto_id_2=auto_id_2)


@app.get("/filter_autos/", response_model=list[pydantic_models.Auto])
def filter_autos(brand: str = "", cost_min: int = 0, cost_max: int = 2**32, age_min: int = 1899,
                 age_max: int = (datetime.now().year), db: Session = Depends(get_db)):
    return sac.filter_autos(db=db, brand=brand,cost_min=cost_min, cost_max=cost_max, age_min=age_min, age_max=age_max)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)