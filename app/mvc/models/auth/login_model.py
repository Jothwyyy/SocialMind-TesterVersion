from mvc.models import supabase_client

def iniciar_sesion_model(email: str, password: str):
    supabase = supabase_client.get_supabase_client()

    try:
        response = supabase.auth.sign_in_with_password({
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

        if "Invalid login credentials" in error_str:
            return {"error": "Correo o contraseña inválidos", "status": False}

        elif "Email not confirmed" in error_str:
            return {"error": "Correo no confirmado", "status": False}

        elif "User not found" in error_str:
            return {"error": "Usuario no encontrado", "status": False}

        else:
            print(f"Error real: {msj_error}")
            return {"error": "Error interno del servidor", "status": False}