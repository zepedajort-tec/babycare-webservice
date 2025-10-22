import requests
import json

# NOTA: Se actualiza el BASE_URL para apuntar al endpoint de padres
BASE_URL = "https://zany-goggles-v6rrq7j5px47fpq5r-8000.app.github.dev/parents"


def pretty_print(response):
    """
    Imprime la respuesta JSON de forma legible.
    """
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Error al decodificar respuesta:", response.text)


def test_create_parent():
    """Prueba la creación de un nuevo padre/madre."""
    print("Creando nuevo padre/madre...")
    data = {
        "name": "Ricardo Perez",
        "email": "ricardo.perez@example.com",
        "phone": "555-123-4567"
    }
    r = requests.post(BASE_URL, json=data)
    print("Status:", r.status_code)
    pretty_print(r)


def test_get_all_parents():
    """Prueba la obtención de todos los padres/madres."""
    print("\nObteniendo todos los padres/madres...")
    r = requests.get(BASE_URL)
    print("Status:", r.status_code)
    pretty_print(r)
    return r.json()


def test_get_parent_by_id(parent_id: int):
    """Prueba la consulta de un padre/madre por su ID."""
    print(f"\nConsultando padre/madre con ID {parent_id}...")
    r = requests.get(f"{BASE_URL}/{parent_id}")
    print("Status:", r.status_code)
    pretty_print(r)


def test_update_parent(parent_id: int):
    """Prueba la actualización de un padre/madre existente."""
    print(f"\nActualizando padre/madre con ID {parent_id}...")
    data = {
        "name": "Ricardo Perez Actualizado",
        "email": "ricardo.a@example.com",
        "phone": "555-999-8888"
    }
    r = requests.put(f"{BASE_URL}/{parent_id}", json=data)
    print("Status:", r.status_code)
    pretty_print(r)


def test_delete_parent(parent_id: int):
    """Prueba la eliminación de un padre/madre por su ID."""
    print(f"\nEliminando padre/madre con ID {parent_id}...")
    r = requests.delete(f"{BASE_URL}/{parent_id}")
    print("Status:", r.status_code)
    pretty_print(r)


if __name__ == "__main__":
    print("Iniciando pruebas del API BabyCare / parents ...\n")

    # 1. Crear registro
    test_create_parent()

    # 2. Leer todos
    parents = test_get_all_parents()

    if parents and isinstance(parents, list) and len(parents) > 0:
        first_id = parents[0]["id"]
        # 3. Leer uno por ID
        test_get_parent_by_id(first_id)
        # 4. Actualizar
        test_update_parent(first_id)
        # 5. Eliminar
        test_delete_parent(first_id)
    else:
        print("\nNo se encontraron registros "
              "para probar los endpoints individuales.")