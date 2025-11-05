from app.db import get_connection

def get_all_parents():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_parents")
        result = cursor.fetchall()
    conn.close()
    return result

def get_parent_by_id(parent_id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_parent", (parent_id,))
        result = cursor.fetchone()
    conn.close()
    return result if result else {"message": "Parent not found"}

def create_parent(name, email, phone, relation, age, sex, password_hash):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_create_parent", (name, email, phone, relation, age, sex, password_hash))
        conn.commit()
    conn.close()
    return {"message": "Parent created successfully"}

def update_parent(id, name, email, phone, relation, age, sex, password_hash):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_update_parent", (id, name, email, phone, relation, age, sex, password_hash))
        conn.commit()
    conn.close()
    return {"message": "Parent updated successfully"}

def delete_parent(id: int):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_delete_parent", (id,))
        conn.commit()
    conn.close()
    return {"message": "Parent deleted successfully"}

def get_parent_by_email(email: str):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_get_parent_by_email", (email,))
        result = cursor.fetchone()
    conn.close()
    return result if result else None