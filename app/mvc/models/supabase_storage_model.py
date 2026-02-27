from mvc.models import supabase_client
from datetime import datetime
from flask import session

supabase_client = supabase_client.get_supabase_client()

def subir_imagen_model(imagen_path):
    try: 
        with open(imagen_path, "rb") as f:
            path = f"publicaciones/{session['id_usuario']}/{str(datetime.now()).replace(' ', '_').replace(':', '-')}_{imagen_path.split('/')[-1]}"
            image_response = supabase_client.storage \
                .from_("SocialMindMedia") \
                .upload(
                    file=f,
                    path=path,
                    file_options={"cache-control": "3600", "upsert": "false"}
                )
        return {"status": True, "error": None, "path": path}
    except Exception as e:
        print(f"Error al subir la imagen: {e}")
        return {"status": False, "error": str(e), "path": None}

def subir_imagen_perfil_model(imagen_path):
    try: 
        with open(imagen_path, "rb") as f:
            path = f"perfiles/{session['id_usuario']}/{str(datetime.now()).replace(' ', '_').replace(':', '-')}_{imagen_path.split('/')[-1]}"
            image_response = supabase_client.storage \
                .from_("SocialMindMedia") \
                .upload(
                    file=f,
                    path=path,
                    file_options={"cache-control": "3600", "upsert": "false"}
                )
        return {"status": True, "error": None, "path": path}
    except Exception as e:
        print(f"Error al subir la imagen de perfil: {e}")
        return {"status": False, "error": str(e), "path": None}

def subir_imagen_banner_model(imagen_path):
    try: 
        with open(imagen_path, "rb") as f:
            path = f"banners/{session['id_usuario']}/{str(datetime.now()).replace(' ', '_').replace(':', '-')}_{imagen_path.split('/')[-1]}"
            image_response = supabase_client.storage \
                .from_("SocialMindMedia") \
                .upload(
                    file=f,
                    path=path,
                    file_options={"cache-control": "3600", "upsert": "false"}
                )
        return {"status": True, "error": None, "path": path}
    except Exception as e:
        print(f"Error al subir la imagen de banner: {e}")
        return {"status": False, "error": str(e), "path": None}
