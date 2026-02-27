from mvc.models.supabase_client import get_supabase_client

supabase_client = get_supabase_client()

def obtener_etiquetas():
    try:
        response = supabase_client.table('intereses').select('*').execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se encontraron etiquetas"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def actualizar_etiquetas_usuario(id_usuario, etiquetas_seleccionadas):
    try:
        supabase_client.table("usuariosintereses").delete().eq("id_usuario", id_usuario).execute()

        if etiquetas_seleccionadas:
            nuevas_etiquetas = [{"id_usuario": id_usuario, "id_interes": int(id_etiqueta)} for id_etiqueta in etiquetas_seleccionadas]
            supabase_client.table("usuariosintereses").insert(nuevas_etiquetas).execute()
        
        return {"status": True, "error": None}  
    except Exception as e:
        return {"status": False, "error": str(e)}
    
def obtener_etiquetas_usuario(id_usuario):
    try:
        response = supabase_client.table("usuariosintereses").select("intereses(tipo_interes)").eq("id_usuario", id_usuario).execute()
        if response.data:
            etiquetas_usuario = [item["intereses"]["tipo_interes"] for item in response.data]
            return {"status": True, "data": etiquetas_usuario, "error": None}  
        else:
            return {"status": True, "data": [], "error": None}  
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}