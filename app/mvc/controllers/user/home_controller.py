from flask import render_template, Blueprint, request, redirect, url_for, session
from mvc.models.user import post_model
from mvc.models.user import current_user_model


home_bp = Blueprint('home', __name__, template_folder='../../views')

@home_bp.route('/inicio')
def inicio_controller():
    current_user = current_user_model.usuario_actual_model(session["email"])
    publicaciones = post_model.publicaciones_model(session["id_usuario"])
    print(publicaciones)
    return render_template('inicio.html', publicaciones=publicaciones, rol=current_user["data"]["id_rol"], id_usuario=session["id_usuario"])