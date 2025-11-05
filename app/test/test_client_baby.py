import requests
import json
from api_urls import BABIES_URL, LOGIN_URL, REGISTER_URL

def pretty_print(response):
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Error al decodificar respuesta:", response.text)

def get_token():
    data = {
        "email": "babytest@email.com",
        "password": "Passw0rd1"
    }
    r = requests.post(LOGIN_URL, json=data)
    if r.status_code == 404:
        reg_data = {
            "name": "Padre Tests",
            "email": data["email"],
            "password": data["password"]
        }
        r = requests.post(REGISTER_URL, json=reg_data)
    pretty_print(r)
    return r.json()["access_token"]

def test_create_baby(token, parent_id):
    print("Creando nuevo bebé...")
    data = {
        "parent_id": parent_id,
        "name": "Luna",
        "age_months": 8,
        "weight": 7.8,
        "height": 67.2
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(BABIES_URL, json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_get_all_babies(token):
    print("\nObteniendo todos los bebés...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(BABIES_URL, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)
    return r.json()

def test_get_baby_by_id(token, baby_id):
    print(f"\nConsultando bebé con ID {baby_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BABIES_URL}/{baby_id}", headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_update_baby(token, baby_id, parent_id):
    print(f"\nActualizando bebé con ID {baby_id}...")
    data = {
        "parent_id": parent_id,
        "name": "Luna Actualizada",
        "age_months": 9,
        "weight": 8.1,
        "height": 68.5
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.put(f"{BABIES_URL}/{baby_id}", json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_delete_baby(token, baby_id):
    print(f"\nEliminando bebé con ID {baby_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{BABIES_URL}/{baby_id}", headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

if __name__ == "__main__":
    print("Iniciando pruebas del API BabyCare...\n")

    # 1. Registrar/Loguear y obtener token
    token = get_token()

    # Obtén el parent_id correspondiente al usuario actual
    # Si la API devolviera el user_id en el login/registro, úsalo:
    parent_id = 1  # Actualízalo según el id del token o el padre creado

    # 2. Crear registro
    test_create_baby(token, parent_id)

    # 3. Leer todos
    babies = test_get_all_babies(token)

    if babies and isinstance(babies, list) and len(babies) > 0:
        first_id = babies[0]["id"]
        # 4. Leer uno por ID
        test_get_baby_by_id(token, first_id)
        # 5. Actualizar
        test_update_baby(token, first_id, parent_id)
        # 6. Eliminar
        test_delete_baby(token, first_id)
    else:
        print("\nNo se encontraron registros para probar los endpoints individuales.")