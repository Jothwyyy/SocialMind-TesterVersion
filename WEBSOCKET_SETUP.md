# Guía de Implementación de WebSockets para Chat en Vivo

## 📋 Cambios Realizados

Se han implementado WebSockets en tu aplicación SocialMind para que los mensajes se visualicen en tiempo real. Aquí está todo lo que ha cambiado:

### 1. **Dependencias Actualizadas**
- Agregué `flask-socketio==5.3.5` a `requirements.txt`

### 2. **Archivos Nuevos/Modificados**

#### Nuevos:
- `app/mvc/controllers/user/websocket_controller.py` - Manejadores de WebSocket
- `app/mvc/views/chat_detalle.html` - Vista del chat con soporte en vivo

#### Modificados:
- `app/main.py` - Configuración de SocketIO y cambio a `socketio.run()`
- `app/mvc/controllers/user/chat_controller.py` - Nueva ruta para ver chat individual
- `app/mvc/models/user/mensajes_model.py` - Nueva función `obtener_mensajes_chat()`
- `app/mvc/models/user/chats_model.py` - Nueva función `obtener_chat_por_id()`
- `app/mvc/controllers/user/crear_chat_controller.py` - Redirección a la vista del chat

---

## 🚀 Instalación y Prueba

### Paso 1: Instalar dependencias
```bash
cd c:\Users\ldgs0\SocialMind-TesterVersion
pip install -r requirements.txt
```

Si tienes problemas con `flask-socketio`, instálalo manualmente:
```bash
pip install flask-socketio==5.3.5
pip install python-socketio==5.10.0
pip install python-engineio==4.8.0
```

### Paso 2: Ejecutar la aplicación
```bash
cd app
python main.py
```

Deberías ver algo como:
```
 * Running on http://0.0.0.0:5000
 * Restarting with reloader
```

### Paso 3: Probar el chat en vivo
1. Abre `http://localhost:5000` en tu navegador
2. Inicia sesión con tu cuenta
3. Ve a `/chats` (Mensajes)
4. Haz clic en un chat existente (o crea uno nuevo)
5. Abre el mismo chat en otra pestaña (con la misma o diferente cuenta)
6. Envía un mensaje - **debería aparecer en vivo sin recargar la página** ✨

---

## 🔌 Cómo Funciona

### En el Servidor (Backend)

El archivo `websocket_controller.py` maneja:

1. **Conexión** (`connect`) - Registra cada usuario conectado
2. **Unirse a sala** (`join`) - Agrega el usuario a una sala de chat específica
3. **Enviar mensaje** (`send_message`) - Recibe mensaje, lo guarda en Supabase y lo emite a todos en la sala
4. **Desconexión** (`disconnect`) - Elimina el usuario de las salas

### En el Cliente (Frontend)

El archivo `chat_detalle.html` incluye:

1. **Conexión Socket.IO** - Conecta al servidor WebSocket
2. **Escucha de eventos** - Recibe mensajes en tiempo real
3. **Envío de mensajes** - Emite mensajes mediante WebSocket
4. **Indicadores visuales** - Muestra estado de conexión y animaciones

---

## 📱 Rutas y URLs

| Ruta | Método | Función |
|------|--------|---------|
| `/chats` | GET | Listar todos los chats del usuario |
| `/chat/<id_chat>` | GET | Ver conversación en vivo |
| `/crear_chat` | POST | Crear chat y primer mensaje |

---

## 🔌 Eventos WebSocket

### Eventos que emite el cliente:
```javascript
socket.emit('join', { chat_id: id_chat })           // Unirse a sala
socket.emit('send_message', { chat_id: id, message: msg }) // Enviar mensaje
socket.emit('leave', { chat_id: id_chat })          // Salir de sala
```

### Eventos que recibe el cliente:
```javascript
socket.on('new_message', (data) => { ... })   // Nuevo mensaje
socket.on('status', (data) => { ... })        // Cambio de estado
socket.on('error', (data) => { ... })         // Errores
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask_socketio'"
**Solución:** Instala las dependencias:
```bash
pip install flask-socketio python-socketio python-engineio
```

### Los mensajes no aparecen en tiempo real
**Verifica:**
1. ✅ El servidor está ejecutándose con `socketio.run()` (no `app.run()`)
2. ✅ Estás en la ruta `/chat/<id_chat>` (no en `/chats`)
3. ✅ La consola del navegador no tiene errores (F12)
4. ✅ Ambas pestaña tienen el mismo `id_chat`

### El indicador de conexión muestra "Desconectado"
**Solución:** Revisa la consola del navegador (F12) para ver errores de WebSocket

---

## 📝 Ejemplo de Flujo de Mensajes

```
Usuario A en localhost:5000/chat/5
    ↓
Escribe mensaje y presiona Enter
    ↓
WebSocket emite: send_message { chat_id: 5, message: "Hola!" }
    ↓
Servidor recibe, guarda en Supabase
    ↓
Servidor emite a sala: new_message { ... }
    ↓
Todos los usuarios en /chat/5 reciben el mensaje al instante
```

---

## 🎨 Personalización

### Cambiar color de mensajes
En `chat_detalle.html`, edita:
```css
.message.sent .message-content {
    background-color: #a259e6;  /* Cambia este color */
    color: white;
}
```

### Cambiar animación
```css
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);  /* Edita aquí */
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

---

## ⚙️ Configuración Avanzada

Si quieres modificar la configuración de SocketIO en `main.py`:

```python
socketio = SocketIO(
    app,
    cors_allowed_origins="*",  # Permitir todas las orígenes
    ping_timeout=60,           # Timeout de ping (segundos)
    ping_interval=25,          # Intervalo de ping (segundos)
    async_mode='threading'     # Modo asíncrono
)
```

---

## ✅ Checklist

- [ ] Instalé `flask-socketio` con pip
- [ ] El servidor corre sin errores
- [ ] Puedo acceder a `http://localhost:5000/chats`
- [ ] Los mensajes aparecen en vivo sin recargar
- [ ] El indicador de conexión muestra verde/azul

---

¡Listo! Ahora tienes chat en vivo con WebSockets. 🎉
