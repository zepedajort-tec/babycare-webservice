from app.db import get_connection


def get_all_parents():
    """
    Recupera todos los registros de padres/madres de la base de datos.
    Llama al procedimiento almacenado 'sp_read_parents'.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_parents")
        result = cursor.fetchall()
    conn.close()
    return result


def get_parent_by_id(parent_id: int):
    """
    Recupera un padre/madre por su ID.
    Llama al procedimiento almacenado 'sp_read_parent'.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc("sp_read_parent", (parent_id,))
        result = cursor.fetchone()  # uno solo
    conn.close()
    return result if result else {"message": "Parent not found"}


def create_parent(name, email, phone, relation):
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