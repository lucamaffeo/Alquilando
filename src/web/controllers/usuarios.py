from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.repositories import user
from werkzeug.security import check_password_hash  # Agregar esta importación

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
        try:
            user.create_user(
                email=data["email"],
                password=data["password"],
                role_id=2,  # Asignar siempre rol usuario (id=2)
                nombre=data.get("nombre"),
                apellido=data.get("apellido"),
                telefono=data.get("telefono"),
                fecha_nacimiento=data.get("fecha_nacimiento"),
            )
            flash("Usuario registrado exitosamente.", "success")
            return redirect(url_for("usuarios.login"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("users/register.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user_data = user.find_user_by_email(data["email"])
        if user_data and check_password_hash(user_data.password, data["password"]):  # Usar check_password_hash
            session["user_id"] = user_data.id
            session["user_role"] = user_data.role.name
            flash("Inicio de sesión exitoso.", "success")
            # Redirigir según el rol
            if user_data.role.name == "admin":
                return redirect(url_for("auth.login_code"))  # Corregido: login_code
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

@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_role", None)
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("usuarios.login"))

@bp.route("/delete/<int:user_id>", methods=["POST"])
def delete(user_id):
    if user.delete_user(user_id):
        flash("Usuario eliminado correctamente.", "success")
    else:
        flash("No se pudo eliminar el usuario.", "error")
    return redirect(url_for("usuarios.index"))

@bp.route("/update/<int:user_id>", methods=["GET", "POST"])
def update(user_id):
    u = user.get_user_by_id(user_id)
    if not u:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("usuarios.index"))
    if request.method == "POST":
        data = request.form
        try:
            user.update_user(
                user_id,
                nombre=data.get("nombre"),
                apellido=data.get("apellido"),
                telefono=data.get("telefono"),
                fecha_nacimiento=data.get("fecha_nacimiento"),
                dni=data.get("dni"),
                # Solo actualizar contraseña si se ingresa una nueva
                password=data["password"] if data.get("password") else None,
            )
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("usuarios.show", user_id=user_id))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("users/register.html", user=u, is_update=True)
