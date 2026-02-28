from flask import Flask, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from mvc.controllers.auth.login_controller import iniciar_sesion_bp
from mvc.controllers.auth.sign_in_controller import registrarse_bp
from mvc.controllers.user.home_controller import home_bp
from mvc.controllers.user.nueva_publicacion_controller import nueva_publicacion_bp
from mvc.controllers.user.ver_perfil_controller import ver_perfil_bp
from mvc.controllers.user.etiquetas_controller import etiquetas_bp
from mvc.controllers.user.editar_perfil_controller import editar_perfil_bp
from mvc.controllers.user.ver_solicitudes_controller import ver_solicitudes_bp   
from mvc.controllers.user.enviar_solicitud_controller import enviar_solicitud_bp
from mvc.controllers.user.ver_amigos_controller import ver_amigos_bp
from mvc.controllers.admin.admin_gestionar_usuario_controller import admin_gestionar_usuario_bp
from mvc.controllers.user.chat_controller import chat_controler_bp
from mvc.controllers.user.crear_chat_controller import crear_chat_bp
from mvc.models.user import mensajes_model
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Needed for flash messages 
app.register_blueprint(iniciar_sesion_bp)
app.register_blueprint(registrarse_bp)
app.register_blueprint(home_bp)
app.register_blueprint(nueva_publicacion_bp)
app.register_blueprint(ver_perfil_bp)
app.register_blueprint(etiquetas_bp)
app.register_blueprint(editar_perfil_bp)
app.register_blueprint(ver_solicitudes_bp)
app.register_blueprint(enviar_solicitud_bp)
app.register_blueprint(ver_amigos_bp)
app.register_blueprint(admin_gestionar_usuario_bp)
app.register_blueprint(chat_controler_bp)
app.register_blueprint(crear_chat_bp)

# ===== WEBSOCKET HANDLERS =====
user_connections = {}

@socketio.on('connect')
def handle_connect(auth=None):
    """Manejar conexión de usuario"""
    user_id = session.get('id_usuario')
    sid = request.sid
    
    if user_id:
        user_connections[sid] = user_id
        print(f"✓ Usuario {user_id} conectado. SID: {sid}")
        emit('status', {'msg': f'Usuario {user_id} conectado'})
    else:
        print(f"✗ Conexión sin usuario. SID: {sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Manejar desconexión de usuario"""
    sid = request.sid
    if sid in user_connections:
        user_id = user_connections.pop(sid)
        print(f"✗ Usuario {user_id} desconectado. SID: {sid}")

@socketio.on('join')
def on_join(data):
    """Unirse a una sala de chat"""
    chat_id = data.get('chat_id')
    user_id = session.get('id_usuario')
    sid = request.sid
    
    print(f"👤 Evento join recibido: chat_id={chat_id}, user_id={user_id}, sid={sid}")
    
    if not chat_id or not user_id:
        print(f"✗ Datos inválidos en join")
        emit('error', {'msg': 'Chat ID o usuario no válido'})
        return
    
    room = f'chat_{chat_id}'
    join_room(room)
    emit('status', {
        'msg': f'Usuario {user_id} se unió al chat',
        'chat_id': chat_id,
        'user_id': user_id
    }, room=room)
    print(f"✓ Usuario {user_id} se unió a la sala {room}")

@socketio.on('send_message')
def handle_send_message(data):
    """Manejar envío de mensaje en tiempo real"""
    chat_id = data.get('chat_id')
    contenido = data.get('message')
    user_id = session.get('id_usuario')
    
    print(f"📨 Evento send_message recibido: chat_id={chat_id}, message='{contenido}', user_id={user_id}")
    
    if not all([chat_id, contenido, user_id]):
        print(f"✗ Datos incompletos: chat_id={chat_id}, contenido={contenido}, user_id={user_id}")
        emit('error', {'msg': 'Datos incompletos'})
        return
    
    try:
        # Guardar mensaje en la base de datos
        print(f"💾 Guardando mensaje en BD...")
        response_mensaje = mensajes_model.enviar_mensaje(chat_id, contenido, user_id)
        
        if response_mensaje['status']:
            print(f"✓ Mensaje guardado exitosamente: {response_mensaje['data']}")
            
            # Obtener ID del mensaje de forma segura
            mensaje_id = None
            if response_mensaje['data'] and len(response_mensaje['data']) > 0:
                mensaje_id = response_mensaje['data'][0].get('id_mensaje') or response_mensaje['data'][0].get('id')
            
            # Crear datos del mensaje
            mensaje_data = {
                'id_chat': chat_id,
                'id_usuario_remitente': user_id,
                'contenido': contenido,
                'timestamp': datetime.now().isoformat(),
                'mensaje_id': mensaje_id
            }
            
            # Emitir a todos en la sala
            room = f'chat_{chat_id}'
            print(f"📤 Emitiendo mensaje a sala {room}: {mensaje_data}")
            emit('new_message', mensaje_data, room=room)
            print(f"✓ Mensaje emitido a la sala {room}")
        else:
            print(f"✗ Error al guardar mensaje: {response_mensaje['error']}")
            emit('error', {'msg': response_mensaje['error']})
            
    except Exception as e:
        print(f"✗ Error al enviar mensaje: {str(e)}")
        import traceback
        traceback.print_exc()
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

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True)