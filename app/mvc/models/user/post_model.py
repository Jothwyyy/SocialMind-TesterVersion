from mvc.models.supabase_client import get_supabase_client
from mvc.models.supabase_storage_model import subir_imagen_model

supabase_client = get_supabase_client()

def publicaciones_model(id_usuario_actual):
    try:
        response = supabase_client.table('publicacion').select('*').neq('id_usuario', id_usuario_actual).execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se encontraron publicaciones"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def crear_publicacion_model(contenido_texto, id_usuario, imagen_path=None):
    try:
        if imagen_path:
            image_response = subir_imagen_model(imagen_path)
            if not image_response["status"]:
                return {"status": False, "data": None, "error": f"Error al subir la imagen: {image_response['error']}"}
            else:
                image_url = supabase_client.storage.from_("SocialMindMedia").get_public_url(image_response["path"])
                response = supabase_client.table("publicacion").insert({"contenido_texto": contenido_texto, "id_usuario": id_usuario, "imagen_path": image_url["publicURL"]}).execute()
        else: 
            response = supabase_client.table("publicacion").insert({"contenido_texto": contenido_texto, "id_usuario": id_usuario}).execute()
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