from app.db import get_connection

def get_all_babies():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_babies")
        result = cursor.fetchall()
    conn.close()
    return result

def get_baby_by_id(baby_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_baby", (baby_id,))
        result = cursor.fetchone()
    conn.close()
    return result if result else {"message": "Baby not found"}

def get_babies_by_parent_id(parent_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_read_babies_by_parent", (parent_id,))
            # Obtener filas del primer result set
            rows = cursor.fetchall()
            # Si el cursor devuelve tuplas, convertir a list[dict]
            if cursor.description and rows and not isinstance(rows[0], dict):
                cols = [col[0] for col in cursor.description]
                result = [dict(zip(cols, row)) for row in rows]
            else:
                result = rows or []
            # Si la librería deja más result sets, opcionalmente consumirlos:
            # while cursor.nextset():
            #     _ = cursor.fetchall()
            return result
    finally:
        conn.close()

def create_baby(parent_id, name, age_months, sex, weight, height):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_create_baby", (parent_id, name, age_months, sex, weight, height))
        conn.commit()
    conn.close()
    return {"message": "Baby created successfully"}

def update_baby(id, parent_id, name, age_months, sex, weight, height):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_update_baby", (id, parent_id, name, age_months, sex, weight, height))
        conn.commit()
    conn.close()
    return {"message": "Baby updated successfully"}

def delete_baby(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_delete_baby", (id,))
        conn.commit()
    conn.close()
    return {"message": "Baby deleted successfully"}