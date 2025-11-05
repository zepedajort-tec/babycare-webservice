import requests
import json
from api_urls import RECORDS_URL, BABIES_URL, LOGIN_URL, REGISTER_URL

def pretty_print(response):
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Error al decodificar respuesta:", response.text)

def get_token():
    data = {
        "email": "recordtest@email.com",
        "password": "Test1234"
    }
    r = requests.post(LOGIN_URL, json=data)
    if r.status_code == 404:
        reg_data = {
            "name": "Prueba Registro",
            "email": data["email"],
            "password": data["password"]
        }
        r = requests.post(REGISTER_URL, json=reg_data)
    pretty_print(r)
    return r.json()["access_token"]

def get_first_baby_id(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(BABIES_URL, headers=headers)
    babies = r.json()
    if babies and isinstance(babies, list) and len(babies) > 0:
        return babies[0]["id"]
    return None

def test_create_record(token, baby_id):
    print("Creando nuevo registro...")
    data = {
        "baby_id": baby_id,
        "date": "2022-10-31",
        "vaccine": "poliomelitis",
        "notes": "feliz halloween"
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(RECORDS_URL, json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_get_all_records(token):
    print("\nObteniendo todos los registros...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(RECORDS_URL, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)
    return r.json()

def test_get_record_by_id(token, record_id):
    print(f"\nConsultando registro con ID {record_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{RECORDS_URL}/{record_id}", headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_update_record(token, record_id, baby_id):
    print(f"\nActualizando registro con ID {record_id}...")
    data = {
        "baby_id": baby_id,
        "date": "2022-12-24",
        "vaccine": "tosferina",
        "notes": "jojojo"
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.put(f"{RECORDS_URL}/{record_id}", json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_delete_record(token, record_id):
    print(f"\nEliminando registro con ID {record_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{RECORDS_URL}/{record_id}", headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

if __name__ == "__main__":
    print("Iniciando pruebas del API BabyCare / records ...\n")

    token = get_token()
    # 1. Obtén un baby_id válido
    baby_id = get_first_baby_id(token)
    if not baby_id:
        print("\nNo hay bebés registrados para realizar pruebas de health_records. Registra como mínimo un bebé y vuelve a intentar.")
    else:
        test_create_record(token, baby_id)
        records = test_get_all_records(token)

        if records and isinstance(records, list) and len(records) > 0:
            first_id = records[0]["id"]
            test_get_record_by_id(token, first_id)
            test_update_record(token, first_id, baby_id)
            test_delete_record(token, first_id)
        else:
            print("\nNo se encontraron registros para probar los endpoints individuales.")