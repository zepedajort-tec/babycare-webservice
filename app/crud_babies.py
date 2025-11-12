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
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_read_baby", (baby_id,))
            row = cursor.fetchone()
            if not row:
                return {"message": "Baby not found"}
            # Si el cursor devuelve tuplas, convertir a dict
            if cursor.description and not isinstance(row, dict):
                cols = [col[0] for col in cursor.description]
                return dict(zip(cols, row))
            return row
    finally:
        conn.close()

def get_babies_by_parent_id(parent_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc("sp_read_babies_by_parent", (parent_id,))
            rows = cursor.fetchall()
            if cursor.description and rows and not isinstance(rows[0], dict):
                cols = [col[0] for col in cursor.description]
                result = [dict(zip(cols, row)) for row in rows]
            else:
                result = rows or []
            return result
    finally:
        conn.close()

def create_baby(parent_id, name, age_months, sex, weight, height):
    """
    Inserta el bebé, obtiene el id insertado y devuelve el registro creado
    como dict. Si no puede obtener el registro, devuelve un mensaje.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # Llamar al stored procedure que hace el INSERT
            cursor.callproc("sp_create_baby", (parent_id, name, age_months, sex, weight, height))
            conn.commit()

            # Obtener el id insertado: SELECT LAST_INSERT_ID()
            cursor.execute("SELECT LAST_INSERT_ID()")
            last = cursor.fetchone()
            new_id = None
            if last:
                # last puede ser tupla (val,) o dict dependiendo del cursor
                new_id = last[0] if isinstance(last, (tuple, list)) else list(last.values())[0]

            if new_id:
                # Obtener el registro creado mediante el stored proc sp_read_baby
                cursor.callproc("sp_read_baby", (new_id,))
                new_row = cursor.fetchone()
                if new_row:
                    if cursor.description and not isinstance(new_row, dict):
                        cols = [col[0] for col in cursor.description]
                        return dict(zip(cols, new_row))
                    return new_row
            # Fallback: si no se pudo recuperar el registro, retornar mensaje
            return {"message": "Baby created successfully"}
    finally:
        conn.close()

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