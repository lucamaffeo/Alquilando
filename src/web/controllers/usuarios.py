from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
import random
import string
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.repositories import user, rol
from werkzeug.security import check_password_hash  # Agregar esta importación
from src.web.helpers.auth import has_permission
from flask_mail import Mail, Message
from src.web.helpers.extensions import mail

bp = Blueprint("usuarios", __name__, url_prefix="/users")

@bp.route("/")
@has_permission("user_index")
def index():
    users_list = user.list_users()
    return render_template("users/index.html", users=users_list)

@bp.route("/<int:user_id>")
def show(user_id):
    u = user.get_user_by_id(user_id)
    return render_template("users/show.html", user=u)

@bp.route("/register", methods=["GET", "POST"])
def register():
    user_obj = None
    if request.method == "POST":
        data = request.form
        try:
            user.create_user(
                email=data["email"],
                password=data["password"],
                role_id=2,  # Asignar siempre rol usuario (id=2)
                nombre=data.get("nombre"),
                dni=data.get("dni"),
                apellido=data.get("apellido"),
                telefono=data.get("telefono"),
                fecha_nacimiento=data.get("fecha_nacimiento"),
            )
            flash("Usuario registrado exitosamente.", "success")
            return redirect(url_for("usuarios.login"))
        except ValueError as e:
            flash(str(e), "error")
            # Si hay error, mantener los datos ingresados
            user_obj = type("UserForm", (), data.to_dict())()
    return render_template("users/register.html", user=user_obj, is_update=False)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user_data = user.find_user_by_email(data["email"])
        if not user_data:
            flash("Usuario no registrado.", "error")
            return redirect(url_for("usuarios.login"))
        if user_data and check_password_hash(user_data.password, data["password"]):
            # Redirigir según el rol
            if user_data.role.name == "admin":
                session["pending_admin_email"] = user_data.email  #TODO: probar si esta linea esta demas
                code = str(random.randint(100000, 999999))
                session["2fa_code"] = code
                session["temp_user_id"] = user_data.id
                session["temp_user_role"] = user_data.role.name
                msg = Message(
                    "Tu código 2FA",
                    sender=current_app.config["MAIL_USERNAME"],
                    recipients=[user_data.email]
                )
                msg.body = f"Tu código es: {code}"
                mail.send(msg)
                flash("Ingrese el código de autenticación.", "info")
                return redirect(url_for("auth.login_code"))
            elif user_data.role.name == "empleado":
                session["user_id"] = user_data.id
                session["user_role"] = user_data.role.name
                flash("Inicio de sesión exitoso.", "success")
                return redirect(url_for("vehiculos.index"))
            else:
                session["user_id"] = user_data.id
                session["user_role"] = user_data.role.name
                flash("Inicio de sesión exitoso.", "success")
                return redirect(url_for("global.inicio_global"))
        flash("Contraseña invalida.", "error")
    return render_template("users/login.html")


@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_role", None)
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("usuarios.login"))

@bp.route("/delete/<int:user_id>", methods=["POST"])
@has_permission("user_delete")
def delete(user_id):
    if user.delete_user(user_id):
        flash("Usuario eliminado correctamente.", "success")
    else:
        flash("No se pudo eliminar el usuario.", "error")
    return redirect(url_for("usuarios.index"))

@bp.route("/register/presencial", methods=["GET", "POST"])
@has_permission("user_create_presencial")
def register_presencial():
    user_obj = None
    if request.method == "POST":
        data = request.form
        password = generar_password_aleatoria()
        try:
            user.create_user(
                email=data["email"],
                password=password,
                role_id=2,  # Siempre usuario registrado
                nombre=data.get("nombre"),
                dni=data.get("dni"),
                apellido=data.get("apellido"),
                telefono=data.get("telefono"),
                fecha_nacimiento=data.get("fecha_nacimiento"),
            )
            enviar_mail(data["email"], password)
            flash("Usuario registrado exitosamente. Se envió la contraseña al email.", "success")
            return redirect(url_for("vehiculos.index"))
        except ValueError as e:
            flash(str(e), "error")
            # Si hay error, mantener los datos ingresados
            user_obj = type("UserForm", (), data.to_dict())()
    return render_template("users/register_presencial.html", user=user_obj, is_update=False)

@bp.route("/update/<int:user_id>", methods=["GET", "POST"])
@has_permission("user_update")
def update(user_id):
    u = user.get_user_by_id(user_id)
    if not u:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("usuarios.index"))
    roles = rol.list_roles()
    if request.method == "POST":
        data = request.form
        try:
            password = data["password"] if data.get("password") else None
            if password == "":
                password = None
            user.update_user(
                user_id,
                nombre=data.get("nombre"),
                apellido=data.get("apellido"),
                telefono=data.get("telefono"),
                # Solo actualizar contraseña si se ingresa una nueva
                password=password,
                # Permitir cambiar el rol solo si el usuario es admin
                role_id=int(data.get("role_id")) if session.get("user_role") == "admin" and data.get("role_id") else u.role_id,
            )
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("usuarios.show", user_id=user_id))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("users/register.html", user=u, is_update=True, roles=roles)
