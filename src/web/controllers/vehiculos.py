from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.repositories import vehiculo
from src.web.helpers.auth import has_permission

bp = Blueprint("vehiculos", __name__, url_prefix="/vehiculos")

@bp.route("/")
@has_permission("vehicle_index")
def index():
    vehiculos_list = vehiculo.list_vehiculos(aptos=True)  # Filtrar solo vehículos aptos
    return render_template("vehiculos/index.html", vehiculos=vehiculos_list)

@bp.route("/<int:id>")
@has_permission("vehicle_show")
def show(id):
    v = vehiculo.get_vehiculo(id)
    return render_template("vehiculos/show.html", vehiculo=v)

@bp.route("/create", methods=["GET", "POST"])
@has_permission("vehicle_create")
def create():
    if request.method == "POST":
        data = request.form
        try:
            vehiculo.create_vehiculo(
                patente=data["patente"],
                categoria=data["categoria"],
                marca=data["marca"],
                modelo=data["modelo"],
                precio=data["precio"],
                anio=data["anio"],
                imagen=data["imagen"],
                asientos=data["asientos"],              
            )
            flash("Vehículo creado exitosamente.", "success")
            return redirect(url_for("vehiculos.index"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("vehiculos/create.html")

@bp.route("/update/<int:id>", methods=["GET", "POST"])
@has_permission("vehicle_update")
def update(id):
    v = vehiculo.get_vehiculo(id)
    if request.method == "POST":
        data = request.form
        try:
            vehiculo.update_vehiculo(
                id,
                patente=data["patente"],
                categoria=data["categoria"],
                marca=data["marca"],
                modelo=data["modelo"],
                precio=data["precio"],
                anio=data["anio"],
                imagen=data["imagen"],
                asientos=data["asientos"],              
            )
            flash("Vehículo actualizado exitosamente.", "success")
            return redirect(url_for("vehiculos.index"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("vehiculos/update.html", vehiculo=v)

@bp.route("/delete/<int:id>", methods=["POST"])
@has_permission("vehicle_delete")
def delete(id):
    try:
        vehiculo.delete_vehiculo(id)
        flash("Vehículo eliminado exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("vehiculos.index"))

