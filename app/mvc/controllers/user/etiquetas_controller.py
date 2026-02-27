from flask import render_template, Blueprint, request, redirect, url_for, session
from mvc.models.user import etiquetas_model
from mvc.models.user import etiquetas_model

etiquetas_bp = Blueprint('etiquetas', __name__, template_folder='../../views')

@etiquetas_bp.route('/editar_etiquetas', methods=['GET', 'POST'])
def etiquetas_controller():
    etiquetas = etiquetas_model.obtener_etiquetas()
    if request.method == 'POST':
        etiquetas_seleccionadas = request.form.getlist('etiquetas')
        response = etiquetas_model.actualizar_etiquetas_usuario(session['id_usuario'], etiquetas_seleccionadas)
        if not response["status"]:
            return {"status": False, "error": f"Error al actualizar etiquetas: {response['error']}"}
        return redirect(url_for('ver_perfil.ver_perfil_controller', id_usuario=session['id_usuario']))
    return render_template('editar_etiquetas.html', etiquetas=etiquetas['data'], id_usuario=session['id_usuario'])