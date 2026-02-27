from flask import render_template, Blueprint, request, redirect, url_for, session
from mvc.models.user import solicitudes_model

ver_solicitudes_bp = Blueprint('ver_solicitudes', __name__, template_folder='../../views')

@ver_solicitudes_bp.route('/ver_solicitudes', methods=['GET', 'POST'])
def ver_solicitudes_controller():
    solicitudes = solicitudes_model.obtener_solicitudes_usuario_model(session["email"])
    print(solicitudes)
    if request.method == 'POST':
        id_solicitud = request.form.get('id_solicitud')
        accion = request.form.get('accion')
        if accion == 'aceptar':
            response = solicitudes_model.aceptar_solicitud_amistad_model(id_solicitud)
        elif accion == 'rechazar':
            response = solicitudes_model.rechazar_solicitud_amistad_model(id_solicitud)
        else:
            return {"status": False, "message": "Acción no válida"}
        
        if response["status"]:
            return redirect(url_for('ver_solicitudes.ver_solicitudes_controller'))
        else:
            return {"status": False, "message": response["error"]}
        
    return render_template('ver_solicitudes.html', solicitudes=solicitudes["data"], id_usuario=session["id_usuario"])