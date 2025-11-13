from app.db import get_connection

def get_all_dev_tips():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_tips")
        result = cursor.fetchall()
    conn.close()
    return result

def get_dev_tip_by_id(tip_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        # No hay SP específica para leer por id en el SQL original;
        # si quieres una SP sp_read_tip_by_id, tendría que añadirse.
        # Aquí intento filtrar en Python sobre el resultado completo.
        cursor.callproc("sp_read_tips_by_id", (tip_id,))
        all_tips = cursor.fetchall()
    conn.close()
    for tip in all_tips:
        # Asumimos que la primera columna es id (según CREATE TABLE)
        if tip and tip[0] == tip_id:
            return tip
    return {"message": "Development tip not found"}

def create_dev_tip(age_range, category, tip_text):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_create_tip", (age_range, category, tip_text))
        conn.commit()
    conn.close()
    return {"message": "Development tip created successfully"}

def update_dev_tip(tip_id, age_range, category, tip_text):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_update_tip", (tip_id, age_range, category, tip_text))
        conn.commit()
    conn.close()
    return {"message": "Development tip updated successfully"}

def delete_dev_tip(tip_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_delete_tip", (tip_id,))
        conn.commit()
    conn.close()
    return {"message": "Development tip deleted successfully"}