from src.core.database import db
from src.core.models.vehiculo import Vehiculo

def create_vehiculo(**kwargs):
    """
    Crea un nuevo vehiculo en la base de datos.

    :param kwargs: Argumentos para crear un nuevo vehiculo.
    :return: El vehiculo creado.
    """
    vehiculo = Vehiculo(**kwargs)
    db.session.add(vehiculo)
    db.session.commit()

    return vehiculo

def get_vehiculo_by_id(vehiculo_id):
    """
    Obtiene un vehiculo por su ID.

    :param vehiculo_id: ID del vehiculo a obtener.
    :return: El vehiculo con el ID especificado, o None si no existe.
    """
    return db.session.query(Vehiculo).filter_by(id=vehiculo_id).first()

def update_vehiculo(vehiculo_id, **kwargs):
    """
    Actualiza un vehiculo existente en la base de datos.

    :param vehiculo_id: ID del vehiculo a actualizar.
    :param kwargs: Argumentos para actualizar el vehiculo.
    :return: El vehiculo actualizado, o None si no existe.
    """
    vehiculo = get_vehiculo_by_id(vehiculo_id)
    if vehiculo:
        for key, value in kwargs.items():
            setattr(vehiculo, key, value)
        db.session.commit()
        return vehiculo
    return None

def delete_vehiculo(vehiculo_id):
    """
    Elimina un vehiculo de la base de datos.

    :param vehiculo_id: ID del vehiculo a eliminar.
    :return: True si se eliminó el vehiculo, False si no existía.
    """
    vehiculo = get_vehiculo_by_id(vehiculo_id)
    if vehiculo:
        db.session.delete(vehiculo)
        db.session.commit()
        return True
    return False

def list_vehiculos(aptos=False):
    """
    Lista todos los vehículos, con opción de filtrar solo los aptos.
    """
    query = db.session.query(Vehiculo)
    if aptos:
        query = query.filter_by(en_mantenimiento=False)
    return query.all()