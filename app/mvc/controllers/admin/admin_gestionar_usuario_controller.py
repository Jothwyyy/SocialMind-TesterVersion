from flask import render_template, Blueprint, session, request, url_for, redirect
from mvc.models.user import users_model
from mvc.models.supabase_client import get_supabase_client
from mvc.models.admin.admin_actualizar_info_usuario_model import admin_actualizar_info_usuario
from mvc.models.supabase_storage_model import subir_imagen_perfil_model, subir_imagen_banner_model
from mvc.models.user.roles_model import obtener_roles

supabase_client = get_supabase_client()

admin_gestionar_usuario_bp = Blueprint('admin_gestionar_usuario', __name__, template_folder='../../views/admin/')

@admin_gestionar_usuario_bp.route('/admin/gestionar_usuario/<int:id_usuario>', methods=['GET', 'POST'])
def admin_gestionar_usuarios_controller(id_usuario):
    data_usuario = users_model.obtener_usuario_por_id_model(id_usuario)
    roles = obtener_roles()
    if data_usuario["status"]:
        data_usuario = data_usuario
        if request.method == 'POST':
            imagen_path = None
            banner_path = None

            if 'foto_path' in request.files:
                imagen_perfil = request.files['foto_path']
                if imagen_perfil.filename != '':
                    imagen_path = f"static/uploads/{id_usuario}_perfil_{imagen_perfil.filename}"
                    imagen_perfil.save(imagen_path)

                    imagen_perfil_supabase = subir_imagen_perfil_model(imagen_path)
                    if imagen_perfil_supabase["status"]:
                        imagen_path_local = imagen_perfil_supabase["path"]
                        imagen_path = supabase_client.storage.from_("SocialMindMedia").get_public_url(imagen_path_local)
                        print(imagen_path_local, imagen_path)

            if 'banner_path' in request.files:
                banner = request.files['banner_path']
                if banner.filename != '':
                    banner_path = f"static/uploads/{id_usuario}_banner_{banner.filename}"
                    banner.save(banner_path)

                    banner_supabase = subir_imagen_banner_model(banner_path)
                    if banner_supabase["status"]:
                        banner_path_local = banner_supabase["path"]
                        banner_path = supabase_client.storage.from_("SocialMindMedia").get_public_url(banner_path_local)
                        print(banner_path_local, banner_path)

            nombre = request.form.get('nombre')
            apellido_paterno = request.form.get('apellido_paterno')
            apellido_materno = request.form.get('apellido_materno')
            username = request.form.get('username')
            genero = request.form.get('genero')
            correo_institucional = request.form.get('correo_institucional')
            edad = request.form.get('edad')
            estado = request.form.get('estado')
            descripcion = request.form.get('descripcion')

            response_update = admin_actualizar_info_usuario(
                id_usuario, nombre, apellido_paterno, apellido_materno,
                username, genero, correo_institucional, edad, estado,
                imagen_path, banner_path, descripcion
            )
            if response_update["status"]:
                print("Hecho")
                return redirect(url_for('admin_gestionar_usuario.admin_gestionar_usuarios_controller', id_usuario=id_usuario))
            else:
                print(response_update["error"])
                return redirect(url_for('admin_gestionar_usuario.admin_gestionar_usuarios_controller', id_usuario=id_usuario, error="No se pudo actualizar el perfil"))
            
    else:
        return {"status": False, "message": data_usuario["error"]}
    return render_template('admin_gestionar_usuarios.html', data_usuario=data_usuario, error=None, roles=roles)