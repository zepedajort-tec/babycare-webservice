import requests

BASE_URL = "http://127.0.0.1:8000"

# Crear un nuevo bebé
baby = {"name": "Luna", "age_months": 6, "weight": 7.2, "height": 65.0}
r = requests.post(f"{BASE_URL}/babies/", json=baby)
print("POST Baby:", r.json())

# Obtener todos los bebés
r = requests.get(f"{BASE_URL}/babies/")
print("GET Babies:", r.json())
