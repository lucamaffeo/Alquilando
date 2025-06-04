from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.repositories.sucursal import list_sucursales, get_sucursal_by_id, create_sucursal, update_sucursal, delete_sucursal
from src.web.helpers.auth import has_permission

bp = Blueprint("sucursales", __name__, url_prefix="/sucursales")

@bp.route("/")
@has_permission("sucursal_index")
def index():
    sucursales = list_sucursales()
    return render_template("sucursales/index.html", sucursales=sucursales)

@bp.route("/<int:id>")
@has_permission("sucursal_show")
def show(id):
    sucursal = get_sucursal_by_id(id)
    if not sucursal:
        flash("Sucursal no encontrada.", "error")
        return redirect(url_for("sucursales.index"))
    return render_template("sucursales/show.html", sucursal=sucursal)

@bp.route("/register", methods=["GET", "POST"])
@has_permission("sucursal_create")
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        ubicacion = request.form.get("ubicacion")
        if not nombre or not ubicacion:
            flash("Todos los campos son obligatorios.", "error")
            return render_template("sucursales/register.html")
        try:
            create_sucursal(nombre=nombre, ubicacion=ubicacion)
            flash("Sucursal creada exitosamente.", "success")
            return redirect(url_for("sucursales.index"))
        except ValueError as e:
            flash(str(e), "error")
            return render_template("sucursales/register.html")
    return render_template("sucursales/register.html")
