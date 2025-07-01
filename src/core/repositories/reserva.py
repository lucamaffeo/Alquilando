from src.core.database import db
from src.core.models.reserva import Reserva


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

def update_reserva_vehiculo_y_adicionales(reserva_id, vehiculo_id, adicionales_ids):
    reserva = Reserva.query.get(reserva_id)
    if reserva:
        reserva.vehiculo_id = vehiculo_id
        from src.core.models.adicional import Adicional
        adicionales_objs = Adicional.query.filter(Adicional.id.in_(adicionales_ids)).all() if adicionales_ids else []
        reserva.adicionales = adicionales_objs
        # No modificar reserva.precio_total_adicionales aquí, solo al crear la reserva
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

