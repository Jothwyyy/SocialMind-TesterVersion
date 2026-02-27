from flask import Blueprint, redirect, url_for, request, session
from mvc.models.user import post_model
from mvc.models import supabase_storage_model
from datetime import datetime
from mvc.models.supabase_client import get_supabase_client
import os

supabase_client = get_supabase_client()
nueva_publicacion_bp = Blueprint('nueva_publicacion', __name__)

import os
from datetime import datetime

@nueva_publicacion_bp.route('/nueva_publicacion', methods=['POST'])
def nueva_publicacion_controller():

    if 'id_usuario' not in session:
        return redirect(url_for('auth.login'))

    contenido = request.form.get('contenido')
    imagen = request.files.get('imagen_post')
    ruta = None

    if not contenido and not imagen:
        return {"status": False, "error": "La publicación no puede estar vacía"}

    if imagen and imagen.filename != '':
        imagen_path = f"static/uploads/{session['id_usuario']}_publicacion_{imagen.filename}"
        imagen.save(imagen_path)
        imagen_publicacion_supabase = supabase_storage_model.subir_imagen_model(imagen_path)
        print(imagen_publicacion_supabase["status"])
        if imagen_publicacion_supabase["status"]:
            imagen_publicacion_path = imagen_publicacion_supabase["path"]
            url_imagen_publicacion = supabase_client.storage.from_("SocialMindMedia").get_public_url(imagen_publicacion_path)
            print(f"URL: {url_imagen_publicacion}")
        else:
            return {"status": False, "error": f"Error al subir la imagen: {imagen_publicacion_supabase["error"]}"}
        ruta = url_imagen_publicacion
    response = post_model.crear_publicacion_model(contenido, session['id_usuario'], ruta)

    if response["status"]:
        return redirect(url_for('home.inicio_controller'))
    else:
        return {"status": False, "error": f"Error al crear la publicación: {response['error']}"}