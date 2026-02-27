from mvc.models.supabase_client import get_supabase_client

supabase_client = get_supabase_client()

def usuario_actual_model(email):
    try:
        response = supabase_client.table('usuarios').select('*').eq('correo_institucional', email).execute()
        id_usuario = response.data[0]['id_usuario']
        if response.data:
            intereses_response = supabase_client.table("usuariosintereses").select("intereses(tipo_interes)").eq("id_usuario", id_usuario).execute()
            return {"status": True, "data": response.data[0], "intereses": intereses_response.data} 
        else:
            return {"status": False, "error": "Usuario no encontrado"}
    except Exception as e:
        return {"status": False, "error": str(e)}