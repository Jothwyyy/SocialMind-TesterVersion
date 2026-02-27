from flask import Blueprint, render_template, request, redirect, url_for, session
from mvc.models.user import users_model
from mvc.models.user import current_user_model
from mvc.models.user.users_model import actualizar_usuario_model
from mvc.models.supabase_storage_model import subir_imagen_perfil_model, subir_imagen_banner_model
from mvc.models import supabase_client
import os

supabase_client = supabase_client.get_supabase_client()

upload_folder = "static/uploads"

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

editar_perfil_bp = Blueprint('editar_perfil', __name__, template_folder='../../views')

@editar_perfil_bp.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil_controller():
    current_user_data = current_user_model.usuario_actual_model(session["email"])

    if request.method == 'POST':
        username = request.form.get('username')
        descripcion = request.form.get('descripcion', '')
        imagen_perfil = request.files.get('imagen_perfil', None)
        imagen_banner = request.files.get('imagen_banner', None)
        imagen_perfil_path = None
        imagen_banner_path = None
        url_imagen_perfil = None
        url_imagen_banner = None

        if imagen_perfil and imagen_perfil.filename != '':
            imagen_perfil_path = f"static/uploads/{session['id_usuario']}_perfil_{imagen_perfil.filename}"
            imagen_perfil.save(imagen_perfil_path)
            imagen_perfil_supabase = subir_imagen_perfil_model(imagen_perfil_path)
            if imagen_perfil_supabase["status"]:
                imagen_perfil_path = imagen_perfil_supabase["path"]
                url_imagen_perfil = supabase_client.storage.from_("SocialMindMedia").get_public_url(imagen_perfil_path)



        if imagen_banner and imagen_banner.filename != '':
            imagen_banner_path = f"static/uploads/{session['id_usuario']}_banner_{imagen_banner.filename}"
            imagen_banner.save(imagen_banner_path)
            imagen_banner_supabase = subir_imagen_banner_model(imagen_banner_path)
            if imagen_banner_supabase["status"]:
                imagen_banner_path = imagen_banner_supabase["path"]
                url_imagen_banner = supabase_client.storage.from_("SocialMindMedia").get_public_url(imagen_banner_path)

        update_result = actualizar_usuario_model(username, descripcion, url_imagen_perfil, url_imagen_banner, session["id_usuario"])
        
        if update_result["status"]:
            return redirect(url_for('ver_perfil.ver_perfil_controller', id_usuario=session["id_usuario"]))
        else:
            current_user_data["error"] = update_result["error"]
    return render_template('editar_perfil.html', current_user_data=current_user_data)