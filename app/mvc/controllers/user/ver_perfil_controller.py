from flask import render_template, Blueprint, request, redirect, url_for, session
from mvc.models.user import users_model
from mvc.models.user import post_model
from mvc.models.user import etiquetas_model

ver_perfil_bp = Blueprint('ver_perfil', __name__, template_folder='../../views')

@ver_perfil_bp.route('/ver_perfil/<int:id_usuario>', methods=['GET', 'POST'])
def ver_perfil_controller(id_usuario):
    user_data = users_model.obtener_usuario_por_id_model(id_usuario)
    is_self = (session["id_usuario"] == id_usuario)
    publicaciones = post_model.publicaciones_otros_usuarios_model(id_usuario)
    etiquetas = etiquetas_model.obtener_etiquetas_usuario(id_usuario)
    return render_template('ver_perfil.html', user_data=user_data["data"], is_self=is_self, publicaciones=publicaciones["data"], etiquetas=etiquetas["data"])