from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash

from src.core.models import user as User  # Assuming you have a User model

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/login-code', methods=['GET', 'POST'])
def login_code():
    if request.method == 'POST':
        code = request.form.get('code')
        if code == '1234':
            # Obtener email temporal y buscar usuario
            email = session.pop("pending_admin_email", None)
            if email:
                from src.core.repositories import user as user_repo
                user_data = user_repo.find_user_by_email(email)
                if user_data:
                    session["user_id"] = user_data.id
                    session["user_role"] = user_data.role.name
                    flash("Inicio de sesión exitoso.", "success")
                    return redirect(url_for('global.inicio_global'))
            flash("Error interno al autenticar.", "error")
        else:
            flash("El código es erróneo.", "error")
    return render_template("users/login-code.html")  # Renderiza la plantilla de login-code
