from flask import render_template, Blueprint, session, redirect, url_for, request
from mvc.models.user import amigos_model

ver_amigos_bp = Blueprint('ver_amigos', __name__)

@ver_amigos_bp.route('/ver_amigos', methods=["GET", "POST"])
def ver_amigos_controller():
    amigos = amigos_model.obtener_amigos_usuario_model(session.get('id_usuario'))
    if request.method == "POST":
        id_usuario1 = request.form.get("id_usuario1")
        id_usuario2 = request.form.get("id_usuario2")
        response = amigos_model.eliminar_amigo_model(id_usuario1, id_usuario2)
        if response["status"]:
            return redirect(url_for('ver_amigos.ver_amigos_controller'))
        else:
            return {"status": False, "message": response["error"]}
    return render_template('ver_amigos.html', amigos=amigos["data"], id_usuario=session.get("id_usuario"))