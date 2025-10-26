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
        result = cursor.fetchone()  # uno solo
    conn.close()
    return result if result else {"message": "Baby not found"}


def create_baby(name, age, weight, height):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_create_baby", (name, age, weight, height))
        conn.commit()
    conn.close()
    return {"message": "Baby created successfully"}


def update_baby(id, name, age, weight, height):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_update_baby", (id, name, age, weight, height))
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
