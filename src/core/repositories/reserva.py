from src.core.database import db
from src.core.models.reserva import Reserva

def obtener_estadisticas(sucursal_id, fecha_inicio, fecha_fin):
    """
    Obtiene estadísticas de reservas por sucursal y rango de fechas.
    """
    return db.session.query(
        Reserva.sucursal_id, db.func.count(Reserva.id).label("cantidad")
    ).filter(
        Reserva.sucursal_id == sucursal_id,
        Reserva.fecha_inicio >= fecha_inicio,
        Reserva.fecha_fin <= fecha_fin
    ).group_by(Reserva.sucursal_id).all()

def create_reserva(**kwargs):
    """
    Crea una nueva reserva.
    """
    reserva = Reserva(**kwargs)
    db.session.add(reserva)
    db.session.commit()
    return reserva

def list_reservas_by_user(user_id):
    """
    Lista reservas de un usuario.
    """
    return Reserva.query.filter_by(user_id=user_id).all()
