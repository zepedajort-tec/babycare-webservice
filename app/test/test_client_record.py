#k
import requests
import json

BASE_URL = "https://zany-goggles-v6rrq7j5px47fpq5r-8000.app.github.dev/records"


def pretty_print(response):
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Error al decodificar respuesta:", response.text)


def test_create_record():
    print("Creando nuevo estado...")
    data = {
        "babyid": 100666,
        "date": "1984-10-31",
        "vaccine": "poliomelitis",
        "notes": "feliz halloween"
    }
    r = requests.post(BASE_URL, json=data)
    print("Status:", r.status_code)
    pretty_print(r)


def test_get_all_records():
    print("\nObteniendo todos los estados...")
    r = requests.get(BASE_URL)
    print("Status:", r.status_code)
    pretty_print(r)
    return r.json()


def test_get_record_by_id(record_id):
    print(f"\nConsultando estado con ID {record_id}...")
    r = requests.get(f"{BASE_URL}/{record_id}")
    print("Status:", r.status_code)
    pretty_print(r)


def test_update_record(record_id):
    print(f"\nActualizando estado con ID {record_id}...")
    data = {
        "babyid": 100777,
        "date": "1984-12-24",
        "vaccine": "tosferina",
        "notes": "jojojo"
    }
    r = requests.put(f"{BASE_URL}/{record_id}", json=data)
    print("Status:", r.status_code)
    pretty_print(r)


def test_delete_record(record_id):
    print(f"\nEliminando estado con ID {record_id}...")
    r = requests.delete(f"{BASE_URL}/{record_id}")
    print("Status:", r.status_code)
    pretty_print(r)


if __name__ == "__main__":
    print("Iniciando pruebas del API BabyCare...\n")

    # 1. Crear registro
    test_create_record()

    # 2. Leer todos
    records = test_get_all_records()

    if records and isinstance(records, list) and len(records) > 0:
        first_id = records[0]["id"]
        # 3. Leer uno por ID
        test_get_record_by_id(first_id)
        # 4. Actualizar
        test_update_record(first_id)
        # 5. Eliminar
        test_delete_record(first_id)
    else:
        print("\nNo se encontraron registros "
              "para probar los endpoints individuales.")
