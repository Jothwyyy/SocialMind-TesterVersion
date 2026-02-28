from flask import Blueprint, render_template, url_for, session, request, jsonify, redirect
from mvc.models.user import chats_model, mensajes_model


crear_chat_bp = Blueprint('crear_chat', __name__, template_folder="../../views")

@crear_chat_bp.route('/crear_chat', methods=['POST'])
def crear_chat_controller():
    if request.method == 'POST':
        contenido = request.form.get("inp_mensaje")
        id_usuario_receptor = request.form.get("id_usuario_receptor")
        print(id_usuario_receptor)
        response_chat = chats_model.crear_chat_model(session["id_usuario"], id_usuario_receptor)
        if response_chat["status"]:
            id_chat = chats_model.buscar_chat_participantes(session["id_usuario"], id_usuario_receptor)["data"]
            response_mensaje = mensajes_model.enviar_mensaje(id_chat, contenido, session["id_usuario"])
            if response_mensaje["status"]:
                # Redirigir a la view del chat creado
                return redirect(url_for('chats.ver_chat_controller', id_chat=id_chat))
            else:
                return {"message": response_mensaje["error"]}
        else:
            return {"message": response_chat["error"]}
