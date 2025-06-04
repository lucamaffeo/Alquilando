from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from src.core.models import user as User  # Assuming you have a User model

auth_bp = Blueprint('auth', __name__)

maxTimeMins = 10 #tiempo de expiracion del codigo de verificacion

@auth_bp.route('/login-code', methods=['GET', 'POST'])
def login_code():
    if request.method == "POST":
        code = request.form["code"]
        if code == session.get("2fa_code"):
            tiempo_2fa = datetime.fromisoformat(session.get("2fa_code_time"))
            if datetime.utcnow() - tiempo_2fa <= timedelta(minutes=maxTimeMins):
                session["user_id"] = session.get("temp_user_id")
                session["user_role"] = session.get("temp_user_role")
                session.pop("2fa_code", None)
                session.pop("temp_user_id", None)
                session.pop("temp_user_role", None)
                flash("Inicio de sesión exitoso.", "success")
            else:
                flash("Se ha agotado el tiempo para ingresar el codigo", "error"); return redirect(url_for("usuarios.login"))
        else: flash("El codigo ingresado es incorrecto", "error"); return redirect(url_for("auth.login_code"))
        return redirect(url_for("usuarios.index"))  # Redirige al index de usuarios después del login exitoso
    return render_template("users/login-code.html")  # Renderiza la plantilla de login-code
