from flask_socketio import emit, join_room, leave_room, rooms
from flask import session
from mvc.models.user import mensajes_model, chats_model
from datetime import datetime

# Diccionario para rastrear conexiones de usuarios
user_connections = {}

def init_websocket_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        """Manejar conexión de usuario"""
        user_id = session.get('id_usuario')
        if user_id:
            user_connections[session.sid] = user_id
            print(f"Usuario {user_id} conectado. SID: {session.sid}")
            emit('status', {'msg': f'Usuario {user_id} conectado'})

    @socketio.on('disconnect')
    def handle_disconnect():
        """Manejar desconexión de usuario"""
        if session.sid in user_connections:
            user_id = user_connections.pop(session.sid)
            print(f"Usuario {user_id} desconectado. SID: {session.sid}")

    @socketio.on('join')
    def on_join(data):
        """Unirse a una sala de chat"""
        chat_id = data.get('chat_id')
        user_id = session.get('id_usuario')
        
        if not chat_id or not user_id:
            emit('error', {'msg': 'Chat ID o usuario no válido'})
            return
        
        room = f'chat_{chat_id}'
        join_room(room)
        emit('status', {
            'msg': f'Usuario {user_id} se unió al chat',
            'chat_id': chat_id,
            'user_id': user_id
        }, room=room)
        print(f"Usuario {user_id} se unió a la sala {room}")

    @socketio.on('send_message')
    def handle_send_message(data):
        """Manejar envío de mensaje en tiempo real"""
        chat_id = data.get('chat_id')
        contenido = data.get('message')
        user_id = session.get('id_usuario')
        
        if not all([chat_id, contenido, user_id]):
            emit('error', {'msg': 'Datos incompletos'})
            return
        
        try:
            # Guardar mensaje en la base de datos
            response_mensaje = mensajes_model.enviar_mensaje(chat_id, contenido, user_id)
            
            if response_mensaje['status']:
                # Obtener datos del usuario para mostrar nombre/avatar (opcional)
                mensaje_data = {
                    'id_chat': chat_id,
                    'id_usuario_remitente': user_id,
                    'contenido': contenido,
                    'timestamp': datetime.now().isoformat(),
                    'mensage_id': response_mensaje['data'][0]['id'] if response_mensaje['data'] else None
                }
                
                # Emitir a todos en la sala
                room = f'chat_{chat_id}'
                emit('new_message', mensaje_data, room=room)
                print(f"Mensaje enviado en chat {chat_id} por usuario {user_id}")
            else:
                emit('error', {'msg': response_mensaje['error']})
                
        except Exception as e:
            print(f"Error al enviar mensaje: {str(e)}")
            emit('error', {'msg': f'Error al enviar mensaje: {str(e)}'})

    @socketio.on('leave')
    def on_leave(data):
        """Salir de una sala de chat"""
        chat_id = data.get('chat_id')
        user_id = session.get('id_usuario')
        
        if chat_id:
            room = f'chat_{chat_id}'
            leave_room(room)
            emit('status', {
                'msg': f'Usuario {user_id} salió del chat',
                'chat_id': chat_id
            }, room=room)
            print(f"Usuario {user_id} salió de la sala {room}")
