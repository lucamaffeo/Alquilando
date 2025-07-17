from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.repositories.reserva import ingresos_total_vehiculos_por_sucursal, list_reservas_by_date_range, list_reservas, list_reservas_con_calificaciones, obtener_vehiculos_mas_alquilados, ingresos_total_vehiculos
# from src.core.repositories.calificaciones import obtener_estadisticas_calificaciones
from collections import defaultdict
from datetime import datetime, timedelta
from src.web.helpers.auth import has_permission


bp = Blueprint("estadisticas", __name__, url_prefix="/estadisticas")


@bp.route("/", methods=["GET", "POST"])
@has_permission("estadisticas_index")
def menu():
    from src.core.repositories.sucursal import list_sucursales

    fecha_inicio = "2020-01-01"
    fecha_fin = datetime.now().date().isoformat()
    sucursal_id = None

    sucursales_objs = list_sucursales()
    sucursales = [{"id": str(s.id), "nombre": s.nombre} for s in sucursales_objs]

    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio") or fecha_inicio
        fecha_fin = request.form.get("fecha_fin") or fecha_fin
        sucursal_id = request.form.get("sucursal_id") or None

    ingresos_total = ingresos_total_vehiculos_por_sucursal(fecha_inicio, fecha_fin, sucursal_id)

    # --- Ordenar los ingresos por año y mes, dejando el total al final ---
    total_key = "Total (todos los tiempos)"
    month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']

    items = list(ingresos_total.items())
    meses = [item for item in items if item[0] != total_key]
    total = [item for item in items if item[0] == total_key]

    def mes_ano_key(item):
        mes, anio = item[0].split()
        return int(anio) * 100 + month_names.index(mes)

    meses_ordenados = sorted(meses, key=mes_ano_key)
    ingresos_ordenados = meses_ordenados + total
    labels = [x[0] for x in ingresos_ordenados]
    data = [x[1] for x in ingresos_ordenados]

    return render_template(
        "estadisticas/layout.html",
        ingresos=ingresos_total,
        labels=labels,
        data=data,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        sucursales=sucursales,
        sucursal_id=sucursal_id
    )



@bp.route("/calificaciones", methods=["GET", "POST"])
@has_permission("estadisticas_calificaciones")
def calificaciones():
    fecha_inicio = request.form.get("fecha_inicio") or "2020-01-01"
    fecha_fin = request.form.get("fecha_fin") or datetime.now().date().isoformat()

    # Filtrar reservas con calificaciones por rango de fechas
    reservas = list_reservas_con_calificaciones()
    reservas_filtradas = [
        r for r in reservas
        if r.fecha_fin and fecha_inicio <= r.fecha_fin.strftime("%Y-%m-%d") <= fecha_fin
    ]

    acumulador = defaultdict(lambda: {"cantidad": 0, "suma_calificacion": 0, "veces_calificado": 0})

    for reserva in reservas_filtradas:
        vehiculo = reserva.vehiculo
        if vehiculo:
            nombre = f"{vehiculo.marca} {vehiculo.modelo_nombre()} {vehiculo.anio}"
            acumulador[nombre]["cantidad"] += 1
            acumulador[nombre]["suma_calificacion"] += reserva.calificacion
            acumulador[nombre]["veces_calificado"] += 1

    # Transformar en lista y calcular el promedio
    resultado = sorted([
        {
            "nombre": nombre,
            "cantidad": datos["cantidad"],
            "calificacion_promedio": round(datos["suma_calificacion"] / datos["cantidad"], 2),
            "veces_calificado": datos["veces_calificado"]
        }
        for nombre, datos in acumulador.items()
    ], key=lambda x: x["calificacion_promedio"], reverse=True)


    print(f"Vehículos con calificaciones: {resultado}")
    return render_template("estadisticas/calificaciones.html", vehiculos=resultado, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)


@bp.route("/promedio-alquileres", methods=["GET", "POST"])
@has_permission("estadisticas_promedio")
def promedio_alquileres():
    from src.core.models.vehiculo import Vehiculo
    from src.core.models.modelo import Modelo
    from src.core.models.reserva import Reserva

    fecha_inicio = "2020-01-01"
    fecha_fin = datetime.now().date().isoformat()
    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio") or fecha_inicio
        fecha_fin = request.form.get("fecha_fin") or fecha_fin

    inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
    fin = datetime.strptime(fecha_fin, "%Y-%m-%d") if fecha_fin else None

    vehiculos_todos = Vehiculo.query.all()
    grupos = {}
    for v in vehiculos_todos:
        modelo_nombre = v.modelo_rel.nombre if v.modelo_rel else ""
        key = (v.marca, modelo_nombre)
        if key not in grupos:
            grupos[key] = 0

    # Solo reservas finalizadas en el rango de fechas
    reservas_finalizadas = Reserva.query.filter(
        Reserva.estado == "finalizada"
    )
    if inicio:
        reservas_finalizadas = reservas_finalizadas.filter(Reserva.fecha_inicio >= inicio)
    if fin:
        reservas_finalizadas = reservas_finalizadas.filter(Reserva.fecha_fin <= fin)
    reservas_finalizadas = reservas_finalizadas.all()

    for reserva in reservas_finalizadas:
        vehiculo = reserva.vehiculo
        if vehiculo:
            modelo_nombre = vehiculo.modelo_rel.nombre if vehiculo.modelo_rel else ""
            key = (vehiculo.marca, modelo_nombre)
            grupos[key] = grupos.get(key, 0) + 1

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
    from src.core.models.reserva import Reserva

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

    # Solo reservas finalizadas en el rango de fechas
    reservas_finalizadas = Reserva.query.filter(
        Reserva.estado == "finalizada",
        Reserva.fecha_inicio >= fecha_inicio,
        Reserva.fecha_fin <= fecha_fin
    ).all()

    # Sumar reservas finalizadas por sucursal
    for reserva in reservas_finalizadas:
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


