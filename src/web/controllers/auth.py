from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash

from src.core.models import user as User  # Assuming you have a User model

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login-code', methods=['GET', 'POST'])
def login_code():
    if request.method == "POST":
        code = request.form["code"]
        if code == session.get("2fa_code"):
            session.pop("2fa_code", None)
            flash("✅ Sesión iniciada como " + session.get('username'))
        else: flash("Código incorrecto")
        return redirect(url_for("global.inicio_global"))
    return render_template("users/login-code.html")  # Renderiza la plantilla de login-code
