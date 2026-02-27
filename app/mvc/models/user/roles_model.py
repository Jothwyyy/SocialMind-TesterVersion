from mvc.models.supabase_client import get_supabase_client

supabase_client = get_supabase_client()

def obtener_roles():
    try:
        response = supabase_client.table("rol").select("*").execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}
        else:
            return {"status": False, "data": None, "error": "Error al consultar los roles"}
    except Exception as e:
        return {"status": False, "data": None, "error": f"Error inesperado: {str(e)}"}