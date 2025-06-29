from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.repositories.reserva import list_reservas_by_date_range, list_reservas
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

    reservas_total= list_reservas()
    alquileres_por_sucursal = {}
    for reserva in reservas_total:
        # Se asume que reserva.vehiculo.sucursal existe y tiene nombre
        sucursal = getattr(getattr(reserva, "vehiculo", None), "sucursal", None)
        if sucursal:
            nombre_sucursal = getattr(sucursal, "nombre", "Desconocida")
            alquileres_por_sucursal[nombre_sucursal] = alquileres_por_sucursal.get(nombre_sucursal, 0) + 1

    sucursales = list(alquileres_por_sucursal.keys())
    alquileres = list(alquileres_por_sucursal.values())
   

    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

        reservas = list_reservas_by_date_range(fecha_inicio, fecha_fin)
        print(f"Reservas encontradas: {len(reservas)}")
        # Agrupar reservas por sucursal
        alquileres_por_sucursal = {}
        for reserva in reservas:
            # Se asume que reserva.vehiculo.sucursal existe y tiene nombre
            sucursal = getattr(getattr(reserva, "vehiculo", None), "sucursal", None)
            if sucursal:
                nombre_sucursal = getattr(sucursal, "nombre", "Desconocida")
                alquileres_por_sucursal[nombre_sucursal] = alquileres_por_sucursal.get(nombre_sucursal, 0) + 1

        sucursales = list(alquileres_por_sucursal.keys())
        alquileres = list(alquileres_por_sucursal.values())

    return render_template("estadisticas/alquileres_por_sucursal.html",
                           sucursales=sucursales,
                           alquileres=alquileres)


