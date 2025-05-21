from flask import Blueprint, render_template, request, flash
from src.core.repositories.sucursal import list_sucursales
from datetime import datetime, timedelta

bp = Blueprint("global", __name__, url_prefix="/global")

@bp.route("/inicio", methods=["GET", "POST"])
def inicio_global():
    sucursales = list_sucursales()
    if request.method == "POST":
        sucursal_id = request.form.get("sucursal")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        if not sucursal_id or not fecha_inicio or not fecha_fin:
            flash("Todos los campos son obligatorios.", "error")
        else:
            flash("Búsqueda realizada con éxito.", "success")
    return render_template(
        "global/inicio.html",
        sucursales=sucursales,
        now=datetime.now,
        timedelta=timedelta
    )
