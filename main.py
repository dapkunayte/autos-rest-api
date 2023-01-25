from fastapi import FastAPI, HTTPException, Request, Depends
import json
import crud, models, pydantic_models
from database import SessionLocal, engine
from sqlalchemy.orm import Session


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