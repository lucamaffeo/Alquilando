from src.core.database import db
from src.core.models.reserva import Reserva
from sqlalchemy import func
from src.core.models.vehiculo import Vehiculo
import calendar
from datetime import datetime

def create_reserva(**kwargs):
    """
    Crea una nueva reserva.
    """
    # Calcular el total de adicionales al momento de la reserva
    adicionales_ids = kwargs.get("adicionales_ids", [])
    precio_total_adicionales = 0.0
    adicionales_objs = []
    if adicionales_ids:
        from src.core.models.adicional import Adicional
        adicionales_objs = Adicional.query.filter(Adicional.id.in_(adicionales_ids)).all()
        precio_total_adicionales = sum(a.precio for a in adicionales_objs)
    # Eliminar adicionales_ids de kwargs si existe
    if "adicionales_ids" in kwargs:
        kwargs.pop("adicionales_ids")
    reserva = Reserva(**kwargs)
    reserva.adicionales = adicionales_objs
    reserva.precio_total_adicionales = precio_total_adicionales
    db.session.add(reserva)
    db.session.commit()
    return reserva

def list_reservas(user_id=None, email=None):
    query = Reserva.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if email:
        from src.core.models.user import User
        user = User.query.filter(User.email.ilike(f"%{email}%")).first()
        if user:
            query = query.filter_by(user_id=user.id)
        else:
            # Si no existe el usuario, devolver lista vacía
            return []
    return query.all()


def list_reservas_by_date_range(fecha_inicio, fecha_fin):
    """
    Lista reservas en un rango de fechas.
    """
    return Reserva.query.filter(Reserva.fecha_inicio >= fecha_inicio, Reserva.fecha_fin <= fecha_fin).all()

def list_reservas_by_user(user_id):
    """
    Lista reservas de un usuario.
    """
    return Reserva.query.filter_by(user_id=user_id).all()

def show_reserva(reserva_id):
    """
    Muestra una reserva por su ID.
    """
    return Reserva.query.get(reserva_id)

def delete_reserva(reserva_id):
    """
    Elimina una reserva por su ID.
    """
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        db.session.delete(reserva)
        db.session.commit()
        return True
    return False

def cancelar_reserva_y_guardar_fecha(reserva_id):
    """
    Cancela una reserva y guarda la fecha de cancelación.
    """
    reserva = Reserva.query.get(reserva_id)
    if reserva and reserva.estado != "cancelada":
        from datetime import date
        reserva.estado = "cancelada"
        reserva.fecha_cancelacion = date.today()
        db.session.commit()
        return reserva
    return None

def get_reservas_by_vehiculo(vehiculo_id):
    from src.core.models.reserva import Reserva
    return Reserva.query.filter(
        ((Reserva.vehiculo_asignado_id == vehiculo_id) & (Reserva.vehiculo_asignado_id != None)) |
        ((Reserva.vehiculo_id == vehiculo_id) & (Reserva.vehiculo_asignado_id == None))
    ).all()

def update_reserva_vehiculo_y_adicionales(reserva_id, vehiculo_asignado_id, adicionales_ids):
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        reserva.vehiculo_asignado_id = vehiculo_asignado_id  # Solo cambia el auto asignado
        from src.core.models.adicional import Adicional
        adicionales_objs = Adicional.query.filter(Adicional.id.in_(adicionales_ids)).all() if adicionales_ids else []
        reserva.adicionales = adicionales_objs
        db.session.commit()
        return reserva
    return None

def calificar_reserva(reserva_id, calificacion, comentario):
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        reserva.calificacion = calificacion
        reserva.comentario = comentario
        db.session.commit()
        return reserva
    return None
def list_reservas_con_calificaciones():
    return Reserva.query.filter(Reserva.calificacion.isnot(None)).all()

def obtener_vehiculos_mas_alquilados(fecha_inicio=None, fecha_fin=None):
    query = (
        db.session.query(
            Vehiculo,
            func.count(Reserva.id).label("cantidad_reservas")
        )
        .join(Reserva, Reserva.vehiculo_id == Vehiculo.id)  # acá se desambigua
        
    )

    if fecha_inicio:
        query = query.filter(Reserva.fecha_inicio >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Reserva.fecha_fin <= fecha_fin)

    resultados = (
        query
        .group_by(Vehiculo.id)
        .order_by(func.count(Reserva.id).desc())
        .all()
    )

    return resultados

def ingresos_total_vehiculos(fecha_inicio=None, fecha_fin=None):
    from src.core.models.reserva import Reserva

    # Si no se pasan fechas, usar todo el rango posible
    default_range = not fecha_inicio and not fecha_fin
    if not fecha_inicio:
        fecha_inicio = "2020-01-01"
    if not fecha_fin:
        fecha_fin = datetime.now().date().isoformat()

    # Buscar reservas finalizadas por fecha_fin y canceladas por fecha_cancelacion
    reservas_finalizadas = Reserva.query.filter(
        Reserva.fecha_fin >= fecha_inicio,
        Reserva.fecha_fin <= fecha_fin,
        Reserva.estado == "finalizada"
    ).all()
    reservas_canceladas = Reserva.query.filter(
        Reserva.fecha_cancelacion != None,
        Reserva.fecha_cancelacion >= fecha_inicio,
        Reserva.fecha_cancelacion <= fecha_fin,
        Reserva.estado == "cancelada"
    ).all()

    ingresos_por_mes = {}
    total_general = 0.0

    # Procesar finalizadas
    for r in reservas_finalizadas:
        total = (r.precio_total_vehiculo or 0) + (r.precio_total_adicionales or 0)
        fecha_ingreso = r.fecha_fin
        ingreso = total
        if fecha_ingreso:
            mes_nombre = calendar.month_name[int(fecha_ingreso.month)]
            clave = f"{mes_nombre} {fecha_ingreso.year}"
            ingresos_por_mes[clave] = ingresos_por_mes.get(clave, 0) + float(ingreso or 0)
            total_general += float(ingreso or 0)

    # Procesar canceladas
    for r in reservas_canceladas:
        total = (r.precio_total_vehiculo or 0) + (r.precio_total_adicionales or 0)
        politica = None
        if r.vehiculo and r.vehiculo.modelo_rel and r.vehiculo.modelo_rel.politica_cancelacion:
            politica = r.vehiculo.modelo_rel.politica_cancelacion.strip().lower()
        else:
            politica = "sin reembolso"
        fecha_ingreso = r.fecha_cancelacion
        if politica in ["sin reembolso"]:
            ingreso = total
        elif politica in ["reembolso parcial", "20% de reembolso"]:
            ingreso = total * 0.8
        elif politica in ["reembolso completo", "100% de reembolso"]:
            ingreso = 0
        else:
            ingreso = total  # fallback
        if fecha_ingreso:
            mes_nombre = calendar.month_name[int(fecha_ingreso.month)]
            clave = f"{mes_nombre} {fecha_ingreso.year}"
            ingresos_por_mes[clave] = ingresos_por_mes.get(clave, 0) + float(ingreso or 0)
            total_general += float(ingreso or 0)

    # Mostrar total solo si es el rango por defecto (sin filtro)
    if default_range and total_general > 0:
        ingresos_por_mes["Total (todos los tiempos)"] = total_general

    return ingresos_por_mes

def create_reserva_en_curso(user_id, vehiculo_id, adicionales_ids, fecha_inicio, fecha_fin, precio_total_vehiculo):
    """
    Crea una reserva en estado 'en curso' para uso de empleados, asignando auto y adicionales.
    """
    from src.core.models.adicional import Adicional
    adicionales_objs = Adicional.query.filter(Adicional.id.in_(adicionales_ids)).all() if adicionales_ids else []
    precio_total_adicionales = sum(a.precio for a in adicionales_objs)
    reserva = Reserva(
        user_id=user_id,
        vehiculo_id=vehiculo_id,
        vehiculo_asignado_id=vehiculo_id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado="en curso",
        precio_total_vehiculo=precio_total_vehiculo,
        precio_total_adicionales=precio_total_adicionales
    )
    reserva.adicionales = adicionales_objs
    db.session.add(reserva)
    db.session.commit()
    return reserva

def finalizar_reserva_empleado(reserva_id, reporte_devolucion):
    """
    Finaliza una reserva en curso, guarda el reporte de devolución, cambia el estado de la reserva a 'finalizada'
    y pone el vehículo asignado en mantenimiento. Además, actualiza fecha_fin al día de hoy.
    """
    reserva = Reserva.query.get(reserva_id)
    if reserva and reserva.estado == "en curso":
        from datetime import date
        reserva.estado = "finalizada"
        reserva.reporte_devolucion = reporte_devolucion
        reserva.fecha_fin = date.today()  # Actualiza la fecha de fin al día de hoy
        # Recalcular el total de adicionales al finalizar (por si hubo cambios)
        adicionales = reserva.adicionales or []
        reserva.precio_total_adicionales = sum(a.precio for a in adicionales)
        # Poner el vehículo asignado en mantenimiento
        if reserva.vehiculo_asignado:
            reserva.vehiculo_asignado.en_mantenimiento = True
        db.session.commit()
        return reserva
    return None

def ingresos_total_vehiculos_por_sucursal(fecha_inicio=None, fecha_fin=None, sucursal_id=None):
    from src.core.models.reserva import Reserva
    from src.core.models.vehiculo import Vehiculo

    if not fecha_inicio:
        fecha_inicio = "2020-01-01"
    if not fecha_fin:
        from datetime import datetime
        fecha_fin = datetime.now().date().isoformat()

    reservas_finalizadas = Reserva.query.join(Vehiculo, Reserva.vehiculo_id == Vehiculo.id)
    reservas_canceladas = Reserva.query.join(Vehiculo, Reserva.vehiculo_id == Vehiculo.id)

    reservas_finalizadas = reservas_finalizadas.filter(
        Reserva.fecha_fin >= fecha_inicio,
        Reserva.fecha_fin <= fecha_fin,
        Reserva.estado == "finalizada"
    )
    reservas_canceladas = reservas_canceladas.filter(
        Reserva.fecha_cancelacion != None,
        Reserva.fecha_cancelacion >= fecha_inicio,
        Reserva.fecha_cancelacion <= fecha_fin,
        Reserva.estado == "cancelada"
    )

    if sucursal_id:
        reservas_finalizadas = reservas_finalizadas.filter(Vehiculo.sucursal_id == sucursal_id)
        reservas_canceladas = reservas_canceladas.filter(Vehiculo.sucursal_id == sucursal_id)

    reservas_finalizadas = reservas_finalizadas.all()
    reservas_canceladas = reservas_canceladas.all()

    import calendar
    ingresos_por_mes = {}
    total_general = 0.0

    for r in reservas_finalizadas:
        total = (r.precio_total_vehiculo or 0) + (r.precio_total_adicionales or 0)
        fecha_ingreso = r.fecha_fin
        ingreso = total
        if fecha_ingreso:
            mes_nombre = calendar.month_name[int(fecha_ingreso.month)]
            clave = f"{mes_nombre} {fecha_ingreso.year}"
            ingresos_por_mes[clave] = ingresos_por_mes.get(clave, 0) + float(ingreso or 0)
            total_general += float(ingreso or 0)

    for r in reservas_canceladas:
        total = (r.precio_total_vehiculo or 0) + (r.precio_total_adicionales or 0)
        politica = None
        if r.vehiculo and r.vehiculo.modelo_rel and r.vehiculo.modelo_rel.politica_cancelacion:
            politica = r.vehiculo.modelo_rel.politica_cancelacion.strip().lower()
        else:
            politica = "sin reembolso"
        fecha_ingreso = r.fecha_cancelacion
        if politica in ["sin reembolso"]:
            ingreso = total
        elif politica in ["reembolso parcial", "20% de reembolso"]:
            ingreso = total * 0.8
        elif politica in ["reembolso completo", "100% de reembolso"]:
            ingreso = 0
        else:
            ingreso = total  # fallback
        if fecha_ingreso:
            mes_nombre = calendar.month_name[int(fecha_ingreso.month)]
            clave = f"{mes_nombre} {fecha_ingreso.year}"
            ingresos_por_mes[clave] = ingresos_por_mes.get(clave, 0) + float(ingreso or 0)
            total_general += float(ingreso or 0)

    if total_general > 0:
        ingresos_por_mes["Total (todos los tiempos)"] = total_general

    return ingresos_por_mes

