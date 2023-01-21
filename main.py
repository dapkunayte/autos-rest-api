from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
from json import JSONEncoder

app = FastAPI()


class Auto(BaseModel):
    id: int
    brand: str
    age: str
    cost: str
    mileage: str
    transmission: str
    engine_power: str
    engines_type: str
    drive_unit: str
    is_sell: str


class AutoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


with open('autos.json', 'r', encoding='utf-8') as f:
    autos = json.load(f)
    print(type(autos))
    f.close()


@app.get("/")
async def read_root():
    return autos


@app.get("/api/autos/get_by_id/{id_auto}")
async def get_by_id(id_auto: int):
    for auto in autos:
        if auto["id"] == id_auto:
            return auto
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/autos/get_by_brand/{brand_auto}")
async def get_by_brand(brand_auto: str):
    result = []
    for auto in autos:
        if brand_auto in auto["brand"]:
            result.append(auto)
    if len(result) > 0:
        return result
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/autos/add_auto/")
async def create_auto(auto: Auto) -> Auto:
    autos.append(auto)
    with open('autos.json', 'w', encoding='utf-8') as f:
        json.dump(autos, f, ensure_ascii=False, indent=4, cls=AutoEncoder)
    return auto


@app.delete("/api/autos/delete_auto/{id_auto}")
async def delete_auto(id_auto: int):
    for auto in autos:
        if auto["id"] == id_auto:
            autos.remove(auto)
            with open('autos.json', 'w', encoding='utf-8') as f:
                json.dump(autos, f, ensure_ascii=False, indent=4, cls=AutoEncoder)
            return {"responseCode": 0}  # успешное выполнение удаления
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/api/autos/compare_autos/{id_auto_1}/{id_auto_2}")
async def compare_autos(id_auto_1: int, id_auto_2: int):
    auto_1 = None
    auto_2 = None
    newer_auto = ""
    cheaper_auto = ""
    for auto in autos:
        if auto["id"] == id_auto_1:
            auto_1 = auto
        if auto["id"] == id_auto_2:
            auto_2 = auto
        if (auto_1 is not None) and (auto_2 is not None):
            break
    if (auto_1 is None) or (auto_2 is None):
        raise HTTPException(status_code=404, detail="Item not found")

    if int(auto_1["age"]) > int(auto_2["age"]):
        newer_auto = auto_1["id"]
    elif int(auto_1["age"]) < int(auto_2["age"]):
        newer_auto = auto_2["id"]
    else:
        newer_auto = "the same"

    if int(auto_1["cost"]) > int(auto_2["cost"]):
        cheaper_auto = auto_2["id"]
    elif int(auto_1["cost"]) < int(auto_2["cost"]):
        cheaper_auto = auto_1["id"]
    else:
        cheaper_auto = "the same"

    return [{"auto_1": auto_1, "auto_2": auto_2,
             "compare_result": [{"newer_auto": newer_auto, "cheaper_auto": cheaper_auto}]}]


@app.patch("/api/autos/update_auto/{id_auto}")
async def update_auto(id_auto: int, request: Request):
    json_param = await request.json()
    if len(json_param.keys()) and list(json_param.keys())[0] == "is_sell":
        for auto in autos:
            if auto["id"] == id_auto:
                auto["is_sell"] = json_param["is_sell"]
                return auto
    return HTTPException(status_code=404, detail="Item not found")
