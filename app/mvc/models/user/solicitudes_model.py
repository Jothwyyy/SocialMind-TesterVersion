from mvc.models import supabase_client
from mvc.models.user import current_user_model

supabase_client = supabase_client.get_supabase_client()

def obtener_solicitudes_usuario_model(email):
    try:
        id_usuario = current_user_model.usuario_actual_model(email)
        response = supabase_client.table("amistades") \
            .select("""
                id_amistad,
                fecha_solicitud,
                usuarios!amistades_id_usuario1_fkey ( username )
            """) \
            .eq("id_usuario2", id_usuario["data"]["id_usuario"]) \
            .eq("estado", "pendiente") \
            .execute()
        if response.data:
            return {"status": True, "data": response.data, "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se encontraron solicitudes"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def enviar_solicitud_amistad_model(id_usuario1, id_usuario2):
    try:
        response = supabase_client.table("amistades").insert({
            "id_usuario1": id_usuario1,
            "id_usuario2": id_usuario2,
            "estado": "pendiente"
        }).execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se pudo enviar la solicitud"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def verificar_solicitud_existente_model(id_usuario1, id_usuario2):
    try:
        response = supabase_client.table('amistades') \
            .select('*') \
            .or_(
                f"and(id_usuario1.eq.{id_usuario1},id_usuario2.eq.{id_usuario2}),"
                f"and(id_usuario1.eq.{id_usuario2},id_usuario2.eq.{id_usuario1})"
            ) \
            .eq('estado', 'pendiente') \
            .execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se encontró una solicitud existente"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def aceptar_solicitud_amistad_model(id_amistad):
    try:
        response = supabase_client.table("amistades").update({"estado": "aceptada"}).eq("id_amistad", id_amistad).execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se pudo aceptar la solicitud"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def rechazar_solicitud_amistad_model(id_amistad):
    try:
        response = supabase_client.table("amistades").update({"estado": "rechazada"}).eq("id_amistad", id_amistad).execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}  
        else:
            return {"status": False, "data": None, "error": "No se pudo rechazar la solicitud"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}