from flask import Blueprint, render_template, request, flash, redirect, url_for
#from src.core.repositories.reserva import obtener_estadisticas, obtener_estadisticas_vehiculos
# from src.core.repositories.calificaciones import obtener_estadisticas_calificaciones

bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


@bp.route("/")
def menu():
    return render_template("estadisticas/layout.html")



@bp.route("/calificaciones")
def calificaciones():
    return render_template("estadisticas/calificaciones.html")


@bp.route("/promedio-alquileres")
def promedio_alquileres():
    return render_template("estadisticas/promedio_alquileres.html")


@bp.route("/alquileres-por-sucursal", methods=["GET", "POST"])
def alquileres_por_sucursal():
    return render_template("estadisticas/alquileres_por_sucursal.html")

