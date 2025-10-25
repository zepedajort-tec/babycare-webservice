from app.db import get_connection

def get_all_records():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_health")
        result = cursor.fetchall()
    conn.close()
    return result


def get_record_by_id(record_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_health", (health_id,))
        result = cursor.fetchone()  # uno solo
    conn.close()
    return result if result else {"message": "Record not found"}


def create_record(babyid, date, vaccine, notes):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_create_health", (babyid, date, vaccine, notes))
        conn.commit()
    conn.close()
    return {"message": "Record created successfully"}


def update_record(id,babyid,date, vaccine, notes):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_update_health", (id,babyid,date, vaccine, notes))
        conn.commit()
    conn.close()
    return {"message": "Record updated successfully"}


def delete_record(id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_delete_health", (id,))
        conn.commit()
    conn.close()
    return {"message": "record deleted successfully"}
