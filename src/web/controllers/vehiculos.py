from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.repositories import vehiculo

bp = Blueprint("vehiculos", __name__, url_prefix="/vehiculos")

@bp.route("/")
def index():
    vehiculos_list = vehiculo.list_vehiculos(aptos=True)  # Filtrar solo vehículos aptos
    return render_template("vehiculos/index.html", vehiculos=vehiculos_list)

@bp.route("/<int:id>")
def show(id):
    v = vehiculo.get_vehiculo(id)
    return render_template("vehiculos/show.html", vehiculo=v)

@bp.route("/<int:id>/mantenimiento", methods=["POST"])
def cambiar_mantenimiento(id):
    vehiculo_data = vehiculo.get_vehiculo(id)
    if not vehiculo_data:
        flash("Vehículo no encontrado.", "error")
        return redirect(url_for("vehiculos.index"))
    
    # Cambiar estado de mantenimiento
    nuevo_estado = not vehiculo_data.en_mantenimiento
    vehiculo.update_vehiculo(id, en_mantenimiento=nuevo_estado)
    mensaje = "Vehículo puesto en mantenimiento." if nuevo_estado else "Vehículo disponible nuevamente."
    flash(mensaje, "success")
    return redirect(url_for("vehiculos.show", id=id))

@bp.route("/inicio")
def inicio_empleado():
    if session.get("user_role") != "empleado":
        flash("Acceso denegado.", "error")
        return redirect(url_for("usuarios.login"))
    vehiculos_list = vehiculo.list_vehiculos()
    return render_template("vehiculos/index.html", vehiculos=vehiculos_list)

