from flask import Flask
from mvc.controllers.auth.login_controller import iniciar_sesion_bp
from mvc.controllers.auth.sign_in_controller import registrarse_bp
from mvc.controllers.user.home_controller import home_bp
from mvc.controllers.user.nueva_publicacion_controller import nueva_publicacion_bp
from mvc.controllers.user.ver_perfil_controller import ver_perfil_bp
from mvc.controllers.user.etiquetas_controller import etiquetas_bp
from mvc.controllers.user.editar_perfil_controller import editar_perfil_bp

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

 # Needed for flash messages 
app.register_blueprint(iniciar_sesion_bp)
app.register_blueprint(registrarse_bp)
app.register_blueprint(home_bp)
app.register_blueprint(nueva_publicacion_bp)
app.register_blueprint(ver_perfil_bp)
app.register_blueprint(etiquetas_bp)
app.register_blueprint(editar_perfil_bp)

if __name__ == '__main__':
    app.run(debug=True)