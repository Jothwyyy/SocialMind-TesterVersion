from flask import render_template, Blueprint, redirect, url_for, request, session
from mvc.models.supabase_storage_model import subir_banner_grupo_model, subir_imagen_grupo_model
from mvc.models.supabase_client import get_supabase_client
from mvc.models.user.grupos_model import crear_grupo

supabase_client = get_supabase_client()

crear_grupo_bp = Blueprint("crear_grupo", __name__, template_folder="../../views")

@crear_grupo_bp.route("/crear_grupo", methods=['GET', 'POST'])
def crear_grupo_controller():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        imagen_grupo = request.files.get("imagen_perfil")
        banner_grupo = request.files.get("imagen_banner")
        imagen_grupo_path = None
        banner_grupo_path = None
        if imagen_grupo and imagen_grupo.filename != '':
            imagen_grupo_path = f"static/uploads/{session['id_usuario']}_grupo_{imagen_grupo.filename}"
            imagen_grupo.save(imagen_grupo_path)
            imagen_perfil_supabase = subir_imagen_grupo_model(imagen_grupo_path)
            if imagen_perfil_supabase["status"]:
                imagen_perfil_path_local = imagen_perfil_supabase["path"]
                imagen_grupo_path = supabase_client.storage.from_("SocialMindMedia").get_public_url(imagen_perfil_path_local)
                print(imagen_grupo_path)
        if banner_grupo and banner_grupo.filename != '':
            banner_grupo_path = f"static/uploads/{session['id_usuario']}_grupo_banner_{imagen_grupo.filename}"
            banner_grupo.save(banner_grupo_path)
            banner_grupo_supabase = subir_banner_grupo_model(banner_grupo_path)
            if banner_grupo_supabase["status"]:
                banner_grupo_path_local = banner_grupo_supabase["path"]
                banner_grupo_path = supabase_client.storage.from_("SocialMindMedia").get_public_url(banner_grupo_path_local)
                print(banner_grupo_path)
        response_create = crear_grupo(id_usuario_creador=session["id_usuario"], nombre=nombre, descripcion=descripcion, foto_grupo_path=imagen_grupo_path, banner_path=banner_grupo_path)
        if response_create["status"]:
            return redirect(url_for("ver_grupos.ver_grupos_controller"))
        else:
            return render_template('crear_grupo.html', error=response_create["error"])

    return render_template('crear_grupo.html', error=None)