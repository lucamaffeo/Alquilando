from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.repositories import sucursal, reserva
from datetime import datetime

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
    sucursales = sucursal.list_sucursales()
    estadisticas = None
    if request.method == "POST":
        sucursal_id = request.form.get("sucursal")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
        if sucursal_id and fecha_inicio and fecha_fin:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            # Buscar reservas de vehículos de esa sucursal en el rango de fechas
            from src.core.models.reserva import Reserva
            from src.core.models.vehiculo import Vehiculo
            total_alquileres = (
                Reserva.query
                .join(Vehiculo, Reserva.vehiculo_id == Vehiculo.id)
                .filter(
                    Vehiculo.sucursal_id == int(sucursal_id),
                    Reserva.fecha_inicio >= fecha_inicio_dt,
                    Reserva.fecha_fin <= fecha_fin_dt
                )
                .count()
            )
            estadisticas = {"total_alquileres": total_alquileres}
    return render_template(
        "estadisticas/alquileres_por_sucursal.html",
        sucursales=sucursales,
        estadisticas=estadisticas
    )

