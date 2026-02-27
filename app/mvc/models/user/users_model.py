from mvc.models.supabase_client import get_supabase_client

supabase_client = get_supabase_client()

def obtener_usuario_por_id_model(id_usuario):
    try:
        response = supabase_client.table('usuarios').select('*').eq('id_usuario', id_usuario).execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}  
        else:
            return {"status": False, "data": None, "error": "Usuario no encontrado"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def actualizar_usuario_model(username, descripcion, imagen_path, banner_path, id_usuario):
    try:
        update_data = {
            "username": username,
            "descripcion": descripcion,
            "foto_path": imagen_path,
            "banner_path": banner_path
        }
        response = supabase_client.table('usuarios').update(update_data).eq('id_usuario', id_usuario).execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}  
        else:
            return {"status": False, "data": None, "error": "Error al actualizar el usuario"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}