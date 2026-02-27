from flask import Blueprint, render_template, request, redirect, url_for, flash
from mvc.models.auth import sing_in_model

registrarse_bp = Blueprint('registrarse', __name__, template_folder='../../views')

@registrarse_bp.route('/registrarse', methods=['GET', 'POST'])
def registrarse_controller():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        auth = sing_in_model.registrarse_model(email, password)
        # Here you would add your registration logic
        if auth["status"]:  # If registration was successful
            flash('Registration successful! Please check your email to confirm your account.', 'success')
            sing_in_model.registrarse_in_db_model(
                nombre=request.form['nombre'],
                apellido_paterno=request.form['apellido_paterno'],
                apellido_materno=request.form['apellido_materno'],
                username=request.form['username'],
                genero=request.form['genero'],
                correo_institucional=request.form['email'],
                edad=int(request.form['edad']),
                id_rol=1
            )
            return redirect(url_for('iniciar_sesion.iniciar_sesion_controller'))  # Redirect to login page
        else:
            return render_template('registrarse.html', msj_error=auth["error"])
    
    return render_template('registrarse.html', msj_error=None)