from mvc.models import supabase_client

supabase_client = supabase_client.get_supabase_client()

def admin_actualizar_info_usuario(
    id_usuario, 
    nombre, 
    apellido_paterno, 
    apellido_materno, 
    username, 
    genero, 
    correo_institucional,
    edad,
    estado,
    foto_path,
    banner_path,
    descripcion
):
    try:
        data = {
            "nombre": nombre,
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "username": username,
            "genero": genero,
            "correo_institucional": correo_institucional,
            "edad": edad,
            "estado": estado,
            "descripcion": descripcion
        }
        if foto_path:
            data["foto_path"] = foto_path
        if banner_path:
            data["banner_path"] = banner_path
        response = supabase_client.table("usuarios").update(data).eq("id_usuario", id_usuario).execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}
        else:
            return {"status": False, "data": None, "error": "No se pudo actualizar la información del usuario"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}