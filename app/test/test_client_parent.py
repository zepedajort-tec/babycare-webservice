import requests
import json
from api_urls import PARENTS_URL, LOGIN_URL, REGISTER_URL

def pretty_print(response):
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Error al decodificar respuesta:", response.text)

def get_token():
    data = {
        "email": "parenttest@email.com",
        "password": "Secret123"
    }
    r = requests.post(LOGIN_URL, json=data)
    if r.status_code == 404:
        reg_data = {
            "name": "Prueba Padre",
            "email": data["email"],
            "password": data["password"]
        }
        r = requests.post(REGISTER_URL, json=reg_data)
    pretty_print(r)
    return r.json()["access_token"]

def test_create_parent(token):
    print("Creando nuevo padre/madre...")
    data = {
        "name": "Ricardo Perez",
        "email": "ricardo.perez@example.com",
        "phone": "555-123-4567",
        "relation": "Father"
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(PARENTS_URL, json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_get_all_parents(token):
    print("\nObteniendo todos los padres/madres...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(PARENTS_URL, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)
    return r.json()

def test_get_parent_by_id(token, parent_id):
    print(f"\nConsultando padre/madre con ID {parent_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{PARENTS_URL}/{parent_id}", headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_update_parent(token, parent_id):
    print(f"\nActualizando padre/madre con ID {parent_id}...")
    data = {
        "name": "Ricardo Perez Actualizado",
        "email": "ricardo.a@example.com",
        "phone": "555-999-8888",
        "relation": "Guardian"
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.put(f"{PARENTS_URL}/{parent_id}", json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_delete_parent(token, parent_id):
    print(f"\nEliminando padre/madre con ID {parent_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{PARENTS_URL}/{parent_id}", headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

if __name__ == "__main__":
    print("Iniciando pruebas del API BabyCare / parents ...\n")

    token = get_token()
    test_create_parent(token)
    parents = test_get_all_parents(token)

    if parents and isinstance(parents, list) and len(parents) > 0:
        first_id = parents[0]["id"]
        test_get_parent_by_id(token, first_id)
        test_update_parent(token, first_id)
        test_get_parent_by_id(token, first_id)
        test_delete_parent(token, first_id)
        test_get_parent_by_id(token, first_id)
    else:
        print("\nNo se encontraron registros para probar los endpoints individuales.")