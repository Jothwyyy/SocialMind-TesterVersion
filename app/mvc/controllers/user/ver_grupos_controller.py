from flask import render_template, redirect, url_for, session, Blueprint
from mvc.models.user.grupos_model import obtener_grupos, obtener_ids_grupos_usuario

ver_grupos_bp = Blueprint('ver_grupos', __name__, template_folder="../../views")

@ver_grupos_bp.route("/ver_grupos", methods=['GET'])
def ver_grupos_controller():

    if "id_usuario" not in session:
        return redirect(url_for("iniciar_sesion.login"))

    id_usuario = session["id_usuario"]

    response_grupos = obtener_grupos()
    response_usuario = obtener_ids_grupos_usuario(id_usuario)

    if not response_grupos["status"] or not response_usuario["status"]:
        return "Error al cargar los grupos"

    grupos = response_grupos["data"]
    grupos_usuario = response_usuario["data"]  # set()

    grupos_info = []

    for grupo in grupos:
        pertenece = grupo["id_grupo"] in grupos_usuario

        grupos_info.append({
            "id_grupo": grupo["id_grupo"],
            "nombre": grupo["nombre"],
            "descripcion": grupo.get("descripcion"),
            "foto_grupo": grupo.get("foto_grupo_path"),
            "banner": grupo.get("banner"),
            "creador": grupo.get("creador"),
            "pertenece": pertenece
        })
    
    print(grupos_info)

    return render_template(
        "ver_grupos.html",
        grupos=grupos_info,
        id_usuario=session["id_usuario"]
    )