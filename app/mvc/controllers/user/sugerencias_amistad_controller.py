from flask import render_template, redirect, url_for, session, Blueprint
from mvc.models.user.users_model import obtener_todos_los_usuarios_model

sugerencias_amistad_bp = Blueprint("sugerencias_amistad", __name__, template_folder="../../views")

@sugerencias_amistad_bp.route("/sugerencias_amistad", methods=['GET'])
def sugerencias_amistad_controller():
    usuarios = obtener_todos_los_usuarios_model(session["id_usuario"])
    return render_template("sugerencias_amistad.html", usuarios=usuarios)
