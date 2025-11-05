import requests
import json
from api_urls import DEV_TIPS_URL, LOGIN_URL, REGISTER_URL

def pretty_print(response):
    try:
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except Exception as e:
        print(e)
        print("Error al decodificar respuesta:", response.text)

def get_token():
    data = {
        "email": "devtiptest@email.com",
        "password": "TipTest123"
    }
    r = requests.post(LOGIN_URL, json=data)
    if r.status_code == 404:
        reg_data = {
            "name": "Tips Tester",
            "email": data["email"],
            "password": data["password"]
        }
        r = requests.post(REGISTER_URL, json=reg_data)
    pretty_print(r)
    return r.json()["access_token"]

def test_create_tip(token):
    print("Creando nuevo tip de desarrollo...")
    data = {
        "age_range": "0-12",
        "category": "Motor",
        "tip_text": "Practica juegos de estimulación temprana."
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(DEV_TIPS_URL, json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_get_all_tips(token):
    print("\nObteniendo todos los tips...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(DEV_TIPS_URL, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)
    return r.json()

def test_update_tip(token, tip_id):
    print(f"\nActualizando tip con ID {tip_id}...")
    data = {
        "age_range": "1-3",
        "category": "Lenguaje",
        "tip_text": "Lee cuentos juntos todos los días."
    }
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.put(f"{DEV_TIPS_URL}/{tip_id}", json=data, headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

def test_delete_tip(token, tip_id):
    print(f"\nEliminando tip con ID {tip_id}...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{DEV_TIPS_URL}/{tip_id}", headers=headers)
    print("Status:", r.status_code)
    pretty_print(r)

if __name__ == "__main__":
    print("Iniciando pruebas del API BabyCare / development_tips ...\n")

    token = get_token()
    test_create_tip(token)
    tips = test_get_all_tips(token)

    if tips and isinstance(tips, list) and len(tips) > 0:
        first_id = tips[0]["id"]
        test_update_tip(token, first_id)
        test_delete_tip(token, first_id)
    else:
        print("\nNo se encontraron registros para probar los endpoints individuales.")