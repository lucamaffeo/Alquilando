from src.core.database import db
from src.core.models.reserva import Reserva


def create_reserva(**kwargs):
    """
    Crea una nueva reserva.
    """
    reserva = Reserva(**kwargs)
    db.session.add(reserva)
    db.session.commit()
    return reserva

def list_reservas(user_id=None):
    """
    Lista todas las reservas o solo las del usuario si se pasa user_id.
    """
    if user_id:
        return Reserva.query.filter_by(user_id=user_id).all()
    return Reserva.query.all()

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

def get_reservas_by_vehiculo(vehiculo_id):
    from src.core.models.reserva import Reserva
    return Reserva.query.filter_by(vehiculo_id=vehiculo_id).all()

