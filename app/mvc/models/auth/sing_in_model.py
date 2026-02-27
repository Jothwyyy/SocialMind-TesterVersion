from mvc.models import supabase_client

supabase = supabase_client.get_supabase_client()

def registrarse_model(email: str, password: str):

    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return {
            "error": None,
            "status": True,
            "user": response.user
        }

    except Exception as msj_error:
        error_str = str(msj_error)

        if "User already registered" in error_str:
            return {"error": "Usuario ya registrado", "status": False}

        elif "Password should be at least 6 characters" in error_str:
            return {"error": "La contraseña debe tener al menos 6 caracteres", "status": False}

        else:
            print(f"Error real: {msj_error}")
            return {"error": "Error interno del servidor", "status": False}
        
def registrarse_in_db_model(
        nombre: str, 
        apellido_paterno: str, 
        apellido_materno: str, 
        username: str, 
        genero: str,
        correo_institucional: str,
        edad: int,
        id_rol: int
):
    try:
        response = supabase.table('usuarios').insert({
            "nombre": nombre,
            "apellido_paterno": apellido_paterno,
            "apellido_materno": apellido_materno,
            "username": username,
            "genero": genero,
            "correo_institucional": correo_institucional,
            "edad": edad,
            "id_rol": id_rol
        }).execute()
        return {
            "error": None,
            "status": True,
            "data": response.data
        }
    except Exception as msj_error:
        print({"error": f"Error al insertar en la base de datos: {msj_error}", "status": False, "data": None})