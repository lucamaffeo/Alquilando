from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash

from src.core.models import user as User  # Assuming you have a User model

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login-code', methods=['GET', 'POST'])
def login_code():
    if request.method == 'POST':
        code = request.form.get('code')
        # Aquí puedes validar el código ingresado
        if code == '1234':  # Ejemplo de código estático
            return redirect(url_for('global.inicio_global'))  # Redirige al inicio
        else:
            flash("El código es erróneo.", "error")
    return render_template("users/login-code.html")  # Renderiza la plantilla de login-code
