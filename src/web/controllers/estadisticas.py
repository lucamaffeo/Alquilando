from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.repositories.reserva import list_reservas_by_date_range, list_reservas, list_reservas_con_calificaciones, obtener_vehiculos_mas_alquilados, ingresos_total_vehiculos
# from src.core.repositories.calificaciones import obtener_estadisticas_calificaciones
from collections import defaultdict
from datetime import datetime, timedelta
from src.web.helpers.auth import has_permission


bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


@bp.route("/", methods=["GET", "POST"])
@has_permission("estadisticas_index")
def menu():
    # Fechas por defecto
    fecha_inicio = "2020-01-01"
    fecha_fin = datetime.now().date().isoformat()
    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio") or fecha_inicio
        fecha_fin = request.form.get("fecha_fin") or fecha_fin
    ingresos_total = ingresos_total_vehiculos(fecha_inicio, fecha_fin)
    return render_template("estadisticas/layout.html", ingresos=ingresos_total, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)



@bp.route("/calificaciones", methods=["GET", "POST"])
@has_permission("estadisticas_calificaciones")
def calificaciones():
    fecha_inicio = request.form.get("fecha_inicio") or "2020-01-01"
    fecha_fin = request.form.get("fecha_fin") or datetime.now().date().isoformat()

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
    ], key=lambda x: x["calificacion_promedio"], reverse=True)


    print(f"Vehículos con calificaciones: {resultado}")
    return render_template("estadisticas/calificaciones.html",vehiculos=resultado)


@bp.route("/promedio-alquileres", methods=["GET", "POST"])
@has_permission("estadisticas_promedio")
def promedio_alquileres():
    from src.core.models.vehiculo import Vehiculo
    from src.core.models.modelo import Modelo

    fecha_inicio = "2020-01-01"
    fecha_fin = datetime.now().date().isoformat()
    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio") or fecha_inicio
        fecha_fin = request.form.get("fecha_fin") or fecha_fin

    # Parseamos las fechas si existen
    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None

    # Obtener todos los modelos y marcas posibles
    vehiculos_todos = Vehiculo.query.all()
    grupos = {}
    for v in vehiculos_todos:
        modelo_nombre = v.modelo_rel.nombre if v.modelo_rel else ""
        key = (v.marca, modelo_nombre)
        if key not in grupos:
            grupos[key] = 0

    # Obtener reservas finalizadas agrupadas por marca/modelo
    from src.core.repositories.reserva import obtener_vehiculos_mas_alquilados
    vehiculos_con_reservas = obtener_vehiculos_mas_alquilados(inicio, fin)
    for vehiculo, cantidad in vehiculos_con_reservas:
        modelo_nombre = vehiculo.modelo_rel.nombre if vehiculo.modelo_rel else ""
        key = (vehiculo.marca, modelo_nombre)
        grupos[key] = grupos.get(key, 0) + cantidad

    # Convertir a lista ordenada por cantidad desc
    agrupados_list = sorted(
        [ (marca, modelo, total) for (marca, modelo), total in grupos.items() ],
        key=lambda x: x[2], reverse=True
    )

    return render_template(
        "estadisticas/promedio_alquileres.html",
        agrupados_list=agrupados_list,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


@bp.route("/alquileres-por-sucursal", methods=["GET", "POST"])
@has_permission("estadisticas_alquileres")
def alquileres_por_sucursal():
    from src.core.repositories.sucursal import list_sucursales

    # Obtener todas las sucursales
    sucursales_objs = list_sucursales()
    sucursales_nombres = [s.nombre for s in sucursales_objs]

    # Inicializar el diccionario con todas las sucursales en 0
    alquileres_por_sucursal = {nombre: 0 for nombre in sucursales_nombres}

    # Filtrar reservas por fechas si corresponde
    fecha_inicio = "2020-01-01"
    fecha_fin = datetime.now().date().isoformat()
    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio") or fecha_inicio
        fecha_fin = request.form.get("fecha_fin") or fecha_fin
        reservas = list_reservas_by_date_range(fecha_inicio, fecha_fin)
    else:
        reservas = list_reservas()

    # Sumar reservas finalizadas por sucursal
    for reserva in reservas:
        sucursal = getattr(getattr(reserva, "vehiculo", None), "sucursal", None)
        if sucursal:
            nombre_sucursal = getattr(sucursal, "nombre", "Desconocida")
            if nombre_sucursal in alquileres_por_sucursal:
                alquileres_por_sucursal[nombre_sucursal] += 1

    sucursales = list(alquileres_por_sucursal.keys())
    alquileres = list(alquileres_por_sucursal.values())

    return render_template("estadisticas/alquileres_por_sucursal.html",
                           sucursales=sucursales,
                           alquileres=alquileres,
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin)


