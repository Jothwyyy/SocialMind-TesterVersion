from flask import redirect, url_for, session, request, Blueprint
from mvc.models.supabase_client import get_supabase_client
from mvc.models import supabase_storage_model
from mvc.models.user import post_model 

supabase_client = get_supabase_client()

nueva_publicacion_grupo_bp = Blueprint("nueva_publicacion_grupo", __name__, template_folder="../../views")

@nueva_publicacion_grupo_bp.route("/nueva_publicacion_grupo", methods=['POST'])
def nueva_publicacion_grupo_controller():
    if request.method == 'POST':
        contenido = request.form.get("contenido")
        imagen = request.files.get("imagen_post")
        id_grupo = request.form.get("id_grupo")
        imagen_path = None
        if imagen and imagen.filename != '':
            imagen_path = f"static/uploads/{session['id_usuario']}_publicacion_{imagen.filename}"
            imagen.save(imagen_path)
            imagen_publicacion_supabase = supabase_storage_model.subir_imagen_model(imagen_path)
            print(imagen_publicacion_supabase["status"])
            if imagen_publicacion_supabase["status"]:
                imagen_publicacion_path_local = imagen_publicacion_supabase["path"]
                imagen_path = supabase_client.storage.from_("SocialMindMedia").get_public_url(imagen_publicacion_path_local)
            else:
                return {"status": False, "error": f"Error al subir la imagen: {imagen_publicacion_supabase["error"]}"}

        response = post_model.crear_publicacion_grupo_model(contenido_texto=contenido, id_usuario=session["id_usuario"], id_grupo=id_grupo, url_imagen=imagen_path)    
        if response["status"]:
            return redirect(url_for('ver_grupo.ver_grupo_controller', id_grupo=id_grupo))
        else:
            return {"status": False, "error": f"Error al crear la publicación: {response['error']}"}
