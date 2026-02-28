from flask import render_template, session, request, Blueprint
from mvc.models.user import chats_model, mensajes_model
chat_controler_bp = Blueprint('chats', __name__, template_folder='../../views')

@chat_controler_bp.route('/chats', methods=['GET'])
def ver_chats_controller():
    chats = chats_model.obtener_chats_usuario(session["id_usuario"])
    print(chats)
    return render_template('chats.html', chats=chats, id_usuario=session["id_usuario"])

@chat_controler_bp.route('/chat/<int:id_chat>', methods=['GET'])
def ver_chat_controller(id_chat):
    """Mostrar conversación de un chat específico"""
    user_id = session.get("id_usuario")
    
    # Obtener los mensajes del chat
    mensajes = mensajes_model.obtener_mensajes_chat(id_chat)
    print(mensajes)
    
    # Obtener información del chat
    chat_info = chats_model.obtener_chat_por_id(id_chat)
    
    return render_template('chat_detalle.html', 
                          id_chat=id_chat, 
                          user_id=user_id,
                          mensajes=mensajes,
                          chat_info=chat_info)

