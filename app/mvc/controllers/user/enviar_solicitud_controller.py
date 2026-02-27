from flask import Blueprint, session, render_template, url_for
from mvc.models.user import solicitudes_model

enviar_solicitud_bp = Blueprint('enviar_solicitud', __name__, template_folder='../../views')

@enviar_solicitud_bp.route('/enviar_solicitud/<int:id_usuario>', methods=['POST'])
def enviar_solicitud_controller(id_usuario):
    response = solicitudes_model.enviar_solicitud_amistad_model(session["id_usuario"], id_usuario)
    if response["status"]:
        return render_template(url_for('ver_perfil.ver_perfil_controller', id_usuario=id_usuario)   )
    else:
        return {"status": False, "message": response["error"]}