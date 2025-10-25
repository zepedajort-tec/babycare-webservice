# By: Elliot Nez Arredondo
from app.db import get_connection

def get_all_status():
    """
    Recupera todos los estados que los padres registran
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_status")
        result = cursor.fetchall()
    conn.close()
    return result


def get_status_by_id(parent_id: int):
   
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_parent", (status_id,))
        result = cursor.fetchone()  # uno solo
    conn.close()
    return result if result else {"message": "status not found"}

"""
def create_status(name, email, phone, relation):
    """
    Crea un nuevo registro de padre/madre, incluyendo el campo 'relation'.
    Llama al procedimiento almacenado 'sp_create_parent'.
    Asume que los campos son 'name', 'email', 'phone' y 'relation'.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        # ¡IMPORTANTE! Se añade 'relation' a la lista de parámetros
        cursor.callproc("sp_create_parent", (name, email, phone, relation))
        conn.commit()
    conn.close()
    return {"message": "Parent created successfully"}


def update_parent(id, name, email, phone, relation):
    """
    Actualiza un registro de padre/madre existente, incluyendo el campo 'relation'.
    Llama al procedimiento almacenado 'sp_update_parent'.
    Asume que los campos son 'id', 'name', 'email', 'phone' y 'relation'.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        # ¡IMPORTANTE! Se añade 'relation' a la lista de parámetros
        cursor.callproc("sp_update_parent", (id, name, email, phone, relation))
        conn.commit()
    conn.close()
    return {"message": "Parent updated successfully"}


def delete_parent(id: int):
    """
    Elimina un registro de padre/madre por su ID.
    Llama al procedimiento almacenado 'sp_delete_parent'.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_delete_parent", (id,))
        conn.commit()
    conn.close()
    return {"message": "Parent deleted successfully"}
    """
