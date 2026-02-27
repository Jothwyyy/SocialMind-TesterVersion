from flask import Blueprint, redirect, url_for, request, session
from mvc.models.user import post_model
from mvc.models import supabase_storage_model
from datetime import datetime
import os

nueva_publicacion_bp = Blueprint('nueva_publicacion', __name__)

@nueva_publicacion_bp.route('/nueva_publicacion', methods=['POST'])
def nueva_publicacion_controller():
    contenido = request.form.get('contenido')
    imagen = request.files.get('imagen')
    ruta=None
    if imagen and imagen.filename != '':
        ruta_local = os.path.join(
            'static', 'publicaciones', f"{session['id_usuario']}/{str(datetime.now()).replace(' ', '_').replace(':', '-')}"
            )
        imagen.save(ruta_local)
        supabase_response = supabase_storage_model.subir_imagen_model(ruta_local)

        if not supabase_response["status"]:
            return {"status": False, "error": f"Error al subir la imagen: {supabase_response['error']}"}
        
        ruta = supabase_response["path"]

    response = post_model.crear_publicacion_model(contenido, session['id_usuario'], ruta)
    if response["status"]:
        return redirect(url_for('home.inicio_controller'))
    else:
        return {"status": False, "error": f"Error al crear la publicación: {response['error']}"}
