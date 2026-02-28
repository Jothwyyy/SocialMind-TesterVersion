from mvc.models.supabase_client import get_supabase_client

supabase_client = get_supabase_client()

def obtener_chats_usuario(id_usuario):
    try:
        # 1. Obtener chats donde participa el usuario
        response = supabase_client.table("chat") \
            .select("id_chat, id_usuario_1, id_usuario_2") \
            .or_(f"id_usuario_1.eq.{id_usuario},id_usuario_2.eq.{id_usuario}") \
            .execute()

        if not response.data:
            return {"status": False, "data": None, "error": "No hay chats"}

        chats = response.data

        # 2. Obtener IDs de los otros usuarios
        otros_ids = []
        for chat in chats:
            if chat["id_usuario_1"] == id_usuario:
                otros_ids.append(chat["id_usuario_2"])
            else:
                otros_ids.append(chat["id_usuario_1"])

        # Evitar lista vacía
        if not otros_ids:
            return {"status": True, "data": [], "error": None}

        # 3. Traer usuarios en UNA sola consulta
        usuarios = supabase_client.table("usuarios") \
            .select("id_usuario, username, foto_path") \
            .in_("id_usuario", otros_ids) \
            .execute()

        usuarios_dict = {u["id_usuario"]: u for u in usuarios.data}

        # 4. Armar resultado final
        resultado = []
        for chat in chats:
            if chat["id_usuario_1"] == id_usuario:
                otro_id = chat["id_usuario_2"]
            else:
                otro_id = chat["id_usuario_1"]

            user = usuarios_dict.get(otro_id)

            resultado.append({
                "id_chat": chat["id_chat"],
                "id_usuario": otro_id,
                "username": user["username"] if user else "Desconocido",
                "foto": user["foto_path"] if user else None
            })

        return {"status": True, "data": resultado, "error": None}

    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}
    
def crear_chat_model(id_usuario_1, id_usuario_2):
    try:
        response = supabase_client.table("chat").insert(
            {
                "id_usuario_1": id_usuario_1,
                "id_usuario_2":id_usuario_2
            }
        ).execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}
        else:
            return {"status": False, "data": None, "error": "No se pudo crear el chat."}
    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}
    
def buscar_chat_participantes(id_usuario_1, id_usuario_2):
    try:
        response = supabase_client.table("chat") \
            .select("id_chat") \
            .or_(
                f"and(id_usuario_1.eq.{id_usuario_1},id_usuario_2.eq.{id_usuario_2}),"
                f"and(id_usuario_1.eq.{id_usuario_2},id_usuario_2.eq.{id_usuario_1})"
            ) \
            .limit(1) \
            .execute()

        if response.data:
            return {
                "status": True,
                "data": response.data[0]["id_chat"],
                "error": None
            }
        else:
            return {
                "status": False,
                "data": None,
                "error": "No existe un chat entre estos usuarios"
            }

    except Exception as e:
        return {
            "status": False,
            "data": None,
            "error": f"Error inesperado: {str(e)}"
        }

def obtener_chat_por_id(id_chat):
    """Obtener información del chat y el otro participante"""
    try:
        response = supabase_client.table("chat") \
            .select("id_chat, id_usuario_1, id_usuario_2") \
            .eq("id_chat", id_chat) \
            .single() \
            .execute()
        
        if response.data:
            return {"status": True, "data": response.data, "error": None}
        else:
            return {"status": False, "data": None, "error": "Chat no encontrado"}
    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}
