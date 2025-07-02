from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.repositories.reserva import list_reservas_by_date_range, list_reservas, list_reservas_con_calificaciones, obtener_vehiculos_mas_alquilados
# from src.core.repositories.calificaciones import obtener_estadisticas_calificaciones
from collections import defaultdict
from datetime import datetime


bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


@bp.route("/")
def menu():
    return render_template("estadisticas/layout.html")



@bp.route("/calificaciones")
def calificaciones():
    fecha_inicio = request.form.get("fecha_inicio")
    fecha_fin = request.form.get("fecha_fin")

    reservas = list_reservas_con_calificaciones()

    acumulador = defaultdict(lambda: {"cantidad": 0, "suma_calificacion": 0})

    for reserva in reservas:
        vehiculo = reserva.vehiculo
        if vehiculo:
            nombre = f"{vehiculo.marca} {vehiculo.modelo_nombre()} {vehiculo.anio}"
            acumulador[nombre]["cantidad"] += 1
            acumulador[nombre]["suma_calificacion"] += reserva.calificacion

    # Transformar en lista y calcular el promedio
    resultado = sorted([
        {
            "nombre": nombre,
            "cantidad": datos["cantidad"],
            "calificacion_promedio": round(datos["suma_calificacion"] / datos["cantidad"], 2)
        }
        for nombre, datos in acumulador.items()
    ], key=lambda x: x["cantidad"], reverse=True)

    print(f"Vehículos con calificaciones: {resultado}")
    return render_template("estadisticas/calificaciones.html",vehiculos=resultado)


@bp.route("/promedio-alquileres", methods=["GET", "POST"])
def promedio_alquileres():

    fecha_inicio = None
    fecha_fin = None
    if request.method == "POST":
        # Obtenemos las fechas del formulario
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")

    # Parseamos las fechas si existen
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None

    vehiculos_con_reservas = obtener_vehiculos_mas_alquilados(inicio, fin)

    return render_template(
        "estadisticas/promedio_alquileres.html",
        vehiculos=vehiculos_con_reservas,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


@bp.route("/alquileres-por-sucursal", methods=["GET", "POST"])
def alquileres_por_sucursal():

    reservas_total= list_reservas()
    alquileres_por_sucursal = {}
    for reserva in reservas_total:
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
            sucursal = getattr(getattr(reserva, "vehiculo", None), "sucursal", None)
            if sucursal:
                nombre_sucursal = getattr(sucursal, "nombre", "Desconocida")
                alquileres_por_sucursal[nombre_sucursal] = alquileres_por_sucursal.get(nombre_sucursal, 0) + 1

        sucursales = list(alquileres_por_sucursal.keys())
        alquileres = list(alquileres_por_sucursal.values())

    return render_template("estadisticas/alquileres_por_sucursal.html",
                           sucursales=sucursales,
                           alquileres=alquileres)


