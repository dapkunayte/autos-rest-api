from fastapi.testclient import TestClient

from main import app

import random

client = TestClient(app)


def test_read_autos_default_params():
  response = client.get("/autos")
  data = response.json()
  assert response.status_code == 200, 'Expected code 200, got another'
  assert any("id" in item for item in data), 'No cars with assigned IDs'


def test_create_auto():
  payload = {
    "brand": "Mazda",
    "age": 2023,
    "cost": 3000000,
    "mileage": "10000 km",
    "is_sell": True
  }
  request = client.post("/autos", json=payload)
  assert request.status_code == 200, 'Expected code 200, got another'
  assert request.json() == payload, 'Creation JSON request is malformed'


def test_get_auto_by_id():
  auto_id = 3
  response = client.get(f"/autos/{auto_id}")
  data = response.json()
  assert response.status_code == 200, 'Expected code 200, got another'
  assert "id" in data and data["id"] == 3, f'Car with ID {auto_id} not found'


def test_update_auto_by_id():
  auto_id = 3
  data = {
    "brand": "Mazda",
    "age": 2023,
    "cost": round(random.uniform(2000000, 3500000), 3),
    "mileage": "20000 km",
    "is_sell": False
  }
  request = client.put(f"/autos/{auto_id}", json=data)
  data_new = request.json()
  assert request.status_code == 200, 'Expected code 200, got another'
  assert data_new['cost'] == data['cost'], 'Cost field not updated'


def test_create_car_and_delete_by_id():
  payload = {
    "brand": "DeleteTest",
    "age": 2023,
    "cost": 3000000,
    "mileage": "10000 km",
    "is_sell": True
  }
  request_create = client.post("/autos", json=payload)
  assert request_create.status_code == 200, 'Expected code 200, got another'
  assert request_create.json() == payload, 'Creation JSON request is malformed'

  response = client.get("/autos")
  car_list = response.json()
  for car in car_list:
    if car["brand"] == "DeleteTest":
      auto_id = car["id"]
      break
  assert auto_id is not None, 'Failed to retrieve created car ID'

  request_delete = client.delete(f"/autos/{auto_id}")
  assert request_delete.status_code == 200, 'Expected code 200, got another'

  request_check = client.get(f"/autos/{auto_id}")
  assert request_check.status_code == 404, 'Expected code 404, got another'
