from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.repositories.sucursal import list_sucursales, get_sucursal_by_id, create_sucursal, update_sucursal, delete_sucursal

bp = Blueprint("sucursales", __name__, url_prefix="/sucursales")

@bp.route("/")
def index():
    sucursales = list_sucursales()
    return render_template("sucursales/index.html", sucursales=sucursales)

@bp.route("/<int:id>")
def show(id):
    sucursal = get_sucursal_by_id(id)
    if not sucursal:
        flash("Sucursal no encontrada.", "error")
        return redirect(url_for("sucursales.index"))
    return render_template("sucursales/show.html", sucursal=sucursal)
