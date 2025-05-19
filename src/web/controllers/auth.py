from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash

from src.core.models import user as User  # Assuming you have a User model

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        session['role'] = user.role  # Assuming the User model has a 'role' attribute

        if user.role == 'admin':
            return redirect(url_for('auth.login_code'))  # Redirect to login-code
        else:
            return redirect(url_for('home.index'))  # Redirect to home page
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@auth_bp.route('/login-code', methods=['GET', 'POST'])
def login_code():
    if request.method == 'POST':
        code = request.form.get('code')
        # Aquí puedes validar el código ingresado
        if code == '1234':  # Ejemplo de código estático
            return redirect(url_for('home.index'))  # Redirige al inicio
        else:
            return jsonify({'error': 'Código inválido'}), 400
    return "Renderiza la plantilla de login-code"

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200