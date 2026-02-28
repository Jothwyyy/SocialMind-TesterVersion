from flask import render_template, Blueprint, redirect, url_for, session
from mvc.models.user import grupos_model

ver_grupo_bp = Blueprint("ver_grupo", __name__, template_folder="../../views")

@ver_grupo_bp.route("/ver_grupo/<int:id_grupo>")
def ver_grupo_controller(id_grupo):
    # Obtener datos del grupo
    grupo_response = grupos_model.obtener_grupo_por_id(id_grupo=id_grupo)
    print(grupo_response)
    
    # Verificar si la solicitud fue exitosa
    if not grupo_response.get("status") or not grupo_response.get("data"):
        return "Grupo no encontrado", 404
    
    # Extraer el primer (y único) grupo de la respuesta
    grupo = grupo_response["data"]

    
    # Obtener miembros del grupo
    miembros_response = grupos_model.obtener_miembros_grupo(id_grupo=id_grupo)
    miembros = miembros_response.get("data", []) if miembros_response.get("status") else []
    
    # Preparar los datos para la plantilla
    return render_template(
        'ver_grupo.html',
        grupo=grupo,
        id_grupo=id_grupo,
        usuario_id=session.get("id_usuario"),
        miembros=miembros
    )