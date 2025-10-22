import requests
import json

BASE_URL = "https://zany-goggles-v6rrq7j5px47fpq5r-8000.app.github.dev/babies"


def pretty_print(response):
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Error al decodificar respuesta:", response.text)


def test_create_baby():
    print("Creando nuevo bebé...")
    data = {
        "name": "Luna",
        "age_months": 8,
        "weight": 7.8,
        "height": 67.2
    }
    r = requests.post(BASE_URL, json=data)
    print("Status:", r.status_code)
    pretty_print(r)


def test_get_all_babies():
    print("\nObteniendo todos los bebés...")
    r = requests.get(BASE_URL)
    print("Status:", r.status_code)
    pretty_print(r)
    return r.json()


def test_get_baby_by_id(baby_id):
    print(f"\nConsultando bebé con ID {baby_id}...")
    r = requests.get(f"{BASE_URL}/{baby_id}")
    print("Status:", r.status_code)
    pretty_print(r)


def test_update_baby(baby_id):
    print(f"\nActualizando bebé con ID {baby_id}...")
    data = {
        "name": "Luna Actualizada",
        "age_months": 9,
        "weight": 8.1,
        "height": 68.5
    }
    r = requests.put(f"{BASE_URL}/{baby_id}", json=data)
    print("Status:", r.status_code)
    pretty_print(r)


def test_delete_baby(baby_id):
    print(f"\nEliminando bebé con ID {baby_id}...")
    r = requests.delete(f"{BASE_URL}/{baby_id}")
    print("Status:", r.status_code)
    pretty_print(r)


if __name__ == "__main__":
    print("Iniciando pruebas del API BabyCare...\n")

    # 1. Crear registro
    test_create_baby()

    # 2. Leer todos
    babies = test_get_all_babies()

    if babies and isinstance(babies, list) and len(babies) > 0:
        first_id = babies[0]["id"]
        # 3. Leer uno por ID
        test_get_baby_by_id(first_id)
        # 4. Actualizar
        test_update_baby(first_id)
        # 5. Eliminar
        test_delete_baby(first_id)
    else:
        print("\nNo se encontraron registros "
              "para probar los endpoints individuales.")
