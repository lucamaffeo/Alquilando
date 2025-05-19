from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.repositories import user

bp = Blueprint("usuarios", __name__, url_prefix="/users")

@bp.route("/")
def index():
    users_list = user.list_users()
    return render_template("users/index.html", users=users_list)

@bp.route("/<int:user_id>")
def show(user_id):
    u = user.get_user_by_id(user_id)
    return render_template("users/show.html", user=u)

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form
        user.create_user(email=data["email"], password=data["password"], role_id=data["role_id"])
        flash("Usuario registrado exitosamente.", "success")
        return redirect(url_for("usuarios.login"))
    return render_template("users/register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user_data = user.find_user_by_email(data["email"])
        if user_data and user_data.check_password(data["password"]):
            session["user_id"] = user_data.id
            session["user_role"] = user_data.role.name
            flash("Inicio de sesión exitoso.", "success")
            
            # Redirigir según el rol
            if user_data.role.name == "administrador":
                return redirect(url_for("estadisticas.menu"))  # Menú de estadísticas
            elif user_data.role.name == "empleado":
                return redirect(url_for("vehiculos.index"))  # Listado de vehículos
            else:
                return redirect(url_for("global.inicio_global"))  # Página principal para clientes
        flash("Credenciales inválidas.", "error")
    return render_template("users/login.html")

@bp.route("/inicio")
def inicio_admin():
    if session.get("user_role") != "administrador":
        flash("Acceso denegado.", "error")
        return redirect(url_for("usuarios.login"))
    users_list = user.list_users()
    return render_template("users/index.html", users=users_list)
