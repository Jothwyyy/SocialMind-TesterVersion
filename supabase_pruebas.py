from app.mvc.models.supabase_client import get_supabase_client

supabase = get_supabase_client()

response = supabase.table("usuariosintereses").select("intereses(tipo_interes)").eq("id_usuario", 1).execute()

print(response.data)