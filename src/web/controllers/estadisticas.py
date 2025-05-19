from flask import Blueprint, render_template, request, flash
from src.core.repositories.reserva import obtener_estadisticas

bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")

@bp.route("/menu")
def menu():
    return render_template("estadisticas/menu.html")

@bp.route("/sucursal", methods=["GET", "POST"])
def por_sucursal():
    if request.method == "POST":
        sucursal_id = request.form.get("sucursal")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        
        if not sucursal_id or not fecha_inicio or not fecha_fin:
            flash("Todos los campos son obligatorios.", "error")
        else:
            estadisticas = obtener_estadisticas(sucursal_id, fecha_inicio, fecha_fin)
            if estadisticas:
                return render_template("estadisticas/resultado.html", estadisticas=estadisticas)
            flash("No se encontraron datos para el rango seleccionado.", "info")
    return render_template("estadisticas/por_sucursal.html")

@bp.route("/vehiculos", methods=["GET"])
def vehiculos():
    estadisticas = obtener_estadisticas_vehiculos()
    return render_template("estadisticas/vehiculos.html", estadisticas=estadisticas)
