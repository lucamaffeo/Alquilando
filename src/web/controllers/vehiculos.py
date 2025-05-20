from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.repositories import vehiculo
from src.web.helpers.auth import has_permission

bp = Blueprint("vehiculos", __name__, url_prefix="/vehiculos")

@bp.route("/")
@has_permission("vehicle_index")
def index():
    vehiculos_list = vehiculo.list_vehiculos()
    return render_template("vehiculos/index.html", vehiculos=vehiculos_list)

@bp.route("/<int:id>")
@has_permission("vehicle_show")
def show(id):
    v = vehiculo.get_vehiculo_by_id(id)
    return render_template("vehiculos/show.html", vehiculo=v)

@bp.route("/register", methods=["GET", "POST"])
@has_permission("vehicle_create")
def register():
    vehiculo_id = request.args.get("id")
    v = vehiculo.get_vehiculo_by_id(vehiculo_id) if vehiculo_id else None
    if request.method == "POST":
        data = request.form
        try:
            if v:
                vehiculo.update_vehiculo(
                    v.id,
                    patente=data["patente"],
                    categoria=data["categoria"],
                    marca=data["marca"],
                    modelo=data["modelo"],
                    precio=data["precio"],
                    anio=data["anio"],
                    imagen=data["imagen"],
                    asientos=data["asientos"],
                    en_mantenimiento=True if data.get("en_mantenimiento") == "on" else False,
                )
                flash("Vehículo actualizado exitosamente.", "success")
            else:
                vehiculo.create_vehiculo(
                    patente=data["patente"],
                    categoria=data["categoria"],
                    marca=data["marca"],
                    modelo=data["modelo"],
                    precio=data["precio"],
                    anio=data["anio"],
                    imagen=data["imagen"],
                    asientos=data["asientos"],
                    en_mantenimiento=True if data.get("en_mantenimiento") == "on" else False,
                )
                flash("Vehículo creado exitosamente.", "success")
            return redirect(url_for("vehiculos.index"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("vehiculos/register.html", vehiculo=v, is_update=bool(v))

@bp.route("/cambiar_estado/<int:id>", methods=["POST"])
@has_permission("vehicle_update")
def cambiar_estado(id):
    v = vehiculo.get_vehiculo_by_id(id)
    if not v:
        flash("Vehículo no encontrado.", "error")
        return redirect(url_for("vehiculos.index"))
    nuevo_estado = not v.en_mantenimiento
    vehiculo.update_estado_vehiculo(id, nuevo_estado)
    if nuevo_estado:
        flash("El vehículo fue puesto en mantenimiento.", "success")
    else:
        flash("El vehículo está activo.", "success")
    return redirect(url_for("vehiculos.show", id=id))

@bp.route("/delete/<int:id>", methods=["POST"])
@has_permission("vehicle_delete")
def delete(id):
    try:
        vehiculo.delete_vehiculo(id)
        flash("Vehículo eliminado exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("vehiculos.index"))

