from mvc.models.supabase_client import get_supabase_client
from mvc.models.user import current_user_model

supabase_client = get_supabase_client()

def obtener_amigos_usuario_model(id_usuario):
    try:
        # Caso 1: tú eres id_usuario1 → trae id_usuario2
        res1 = supabase_client.table('amistades') \
            .select('usuarios!amistades_id_usuario2_fkey(id_usuario, username, foto_path)') \
            .eq('id_usuario1', id_usuario) \
            .eq('estado', 'aceptada') \
            .execute()

        # Caso 2: tú eres id_usuario2 → trae id_usuario1
        res2 = supabase_client.table('amistades') \
            .select('usuarios!amistades_id_usuario1_fkey(id_usuario, username, foto_path)') \
            .eq('id_usuario2', id_usuario) \
            .eq('estado', 'aceptada') \
            .execute()

        amigos = []

        # Procesar resultados
        if res1.data:
            for item in res1.data:
                amigos.append(item['usuarios'])

        if res2.data:
            for item in res2.data:
                amigos.append(item['usuarios'])

        return {"status": True, "data": amigos, "error": None}

    except Exception as e:
        return {"status": False, "data": None, "error": str(e)}
    
def eliminar_amigo_model(id_usuario1, id_usuario2):
    try:
        response = supabase_client.table('amistades') \
            .delete() \
            .or_(
                f"and(id_usuario1.eq.{id_usuario1},id_usuario2.eq.{id_usuario2}),"
                f"and(id_usuario1.eq.{id_usuario2},id_usuario2.eq.{id_usuario1})"
            ) \
            .execute()
        if response.data:
            return {"status": True, "data": response.data[0], "error": None}
        else:
            return {"status": False, "data": None, "error": "No se pudo eliminar la amistad"}
    except Exception as e:
        return {"status": False, "data": None, "error": str(e)} 