from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from mvc.models.auth import login_model
from mvc.models.user import current_user_model

iniciar_sesion_bp = Blueprint('iniciar_sesion', __name__, template_folder='../../views')

@iniciar_sesion_bp.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion_controller():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        auth = login_model.iniciar_sesion_model(email, password)
        # Here you would add your authentication logic
        if auth["status"]:  # If login was successful
            flash('Login successful!', 'success')
            user_data = current_user_model.usuario_actual_model(email)
            session['email'] = email
            session['id_usuario'] = user_data["data"]["id_usuario"]  # Store user data in session
            return redirect(url_for('home.inicio_controller'))  # Redirect to home page
        else:
            return render_template('iniciar_sesion.html', msj_error=auth["error"])
    
    return render_template('iniciar_sesion.html', msj_error=None)