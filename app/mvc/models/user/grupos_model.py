from mvc.models.supabase_client import get_supabase_client

supabase_client = get_supabase_client()


def obtener_grupos():
    try:
        response = supabase_client.table("grupo")\
            .select("*")\
            .execute()

        if response.data:
            return {
                "status": True,
                "data": response.data,
                "error": None
            }
        else:
            return {
                "status": True,  # no es error, solo no hay grupos
                "data": [],
                "error": None
            }

    except Exception as e:
        return {
            "status": False,
            "data": None,
            "error": f"Error inesperado: {str(e)}"
        }


def obtener_ids_grupos_usuario(id_usuario):
    try:
        response = supabase_client.table("grupousuario")\
            .select("id_grupo")\
            .eq("id_usuario", id_usuario)\
            .execute()

        if response.data:
            ids = set([row["id_grupo"] for row in response.data])
            return {
                "status": True,
                "data": ids,
                "error": None
            }
        else:
            return {
                "status": True,
                "data": set(),
                "error": None
            }

    except Exception as e:
        return {
            "status": False,
            "data": None,
            "error": f"Error inesperado: {str(e)}"
        }
    
def crear_grupo(id_usuario_creador, nombre, descripcion, foto_grupo_path, banner_path):
    try:
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
            "propietario": id_usuario_creador,
        }
        if foto_grupo_path:
            data["foto_grupo_path"] = foto_grupo_path
        if banner_path:
            data["banner"] = banner_path
        response = supabase_client.table("grupo").insert(data).execute()
        if response.data:
            response_unir = supabase_client.table("grupousuario").insert(
                {
                    "id_grupo": response.data[0]["id_grupo"],
                    "id_usuario": id_usuario_creador
                }
            ).execute()
            if response_unir:
                return {"status": True, "data": response_unir.data, "error": None}
            else:
                return {"status": False, "data": None, "error": "Error al unirse al grupo"}
        else:
            return {"status": False, "data": None, "error": "Error al crear el grupo"}
    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}
    
def obtener_grupo_por_id(id_grupo):
    try:
        response = supabase_client.table("grupo") \
            .select("*") \
            .eq("id_grupo", id_grupo) \
            .execute()

        if response.data:
            grupo = response.data[0]

            publicaciones_grupo = supabase_client.table("publicacion") \
                .select("""
                    id_publicacion,
                    contenido_texto,
                    fecha_publicacion,
                    imagen_path,
                    cantidad_likes,
                    cantidad_comentarios,
                    usuarios (
                        id_usuario,
                        nombre,
                        apellido_paterno,
                        username,
                        foto_path
                    )
                """) \
                .eq("id_grupo", id_grupo) \
                .order("fecha_publicacion", desc=True) \
                .execute()

            # 👇 Aquí agregas las publicaciones al grupo
            grupo["publicaciones"] = publicaciones_grupo.data if publicaciones_grupo.data else []

            return {"status": True, "data": grupo, "error": None}

        else:
            return {"status": False, "data": None, "error": "Grupo no encontrado"}

    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}

def obtener_miembros_grupo(id_grupo):
    try:
        response = supabase_client.table("grupousuario")\
            .select("id_usuario, usuarios(id_usuario, username, foto_perfil)")\
            .eq("id_grupo", id_grupo)\
            .execute()
        
        if response.data:
            return {"status": True, "data": response.data, "error": None}
        else:
            return {"status": True, "data": [], "error": None}
    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}