from mvc.models.supabase_client import get_supabase_client
from mvc.models.supabase_storage_model import subir_imagen_model

supabase_client = get_supabase_client()

def publicaciones_model(id_usuario_actual):
    try:
        response = supabase_client.table('publicacion') \
            .select("""
                id_publicacion,
                contenido_texto,
                fecha_publicacion,
                imagen_path,
                cantidad_likes,
                cantidad_comentarios,
                id_usuario,
                usuarios (
                    username,
                    foto_path
                )
            """) \
            .neq('id_usuario', id_usuario_actual) \
            .execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se encontraron publicaciones"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def crear_publicacion_model(contenido_texto, id_usuario, url_imagen=None):
    try:
        data = {
            "contenido_texto": contenido_texto,
            "id_usuario": id_usuario
        }
        if url_imagen:
            data["imagen_path"] = url_imagen
        response = supabase_client.table("publicacion").insert(data).execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None} 
        else:
            return {"status": False, "data": None, "error": "No se pudo crear la publicación"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def publicaciones_otros_usuarios_model(id_usuario):
    try:
        response = supabase_client.table('publicacion').select('*').eq('id_usuario', id_usuario).execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se encontraron publicaciones"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}