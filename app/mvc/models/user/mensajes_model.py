from mvc.models.supabase_client import get_supabase_client

supabase_client = get_supabase_client()

def enviar_mensaje(id_chat, contenido, id_usuario_remitente):
    try:
        response = supabase_client.table("mensajes").insert(
            {
                "contenido": contenido,
                "id_usuario_remitente": id_usuario_remitente,
                "id_chat": id_chat
            }
        ).execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}
        else:
            return {"status": False, "data": None, "error": "No se pudo enviar el mensaje"}
    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}

def obtener_mensajes_chat(id_chat):
    """Obtener todos los mensajes de un chat ordenados por fecha"""
    try:
        response = supabase_client.table("mensajes") \
            .select("id_mensaje, contenido, id_usuario_remitente, id_chat, fecha_envio") \
            .eq("id_chat", id_chat) \
            .order("fecha_envio", desc=False) \
            .execute()
        
        if response.data:
            return {"status": True, "data": response.data, "error": None}
        else:
            return {"status": True, "data": [], "error": None}
    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}
