from src.core.database import db
from src.core.models.vehiculo import Vehiculo

def create_vehiculo(**kwargs):
    """
    Crea un nuevo vehiculo en la base de datos.

    :param kwargs: Argumentos para crear un nuevo vehiculo.
    :return: El vehiculo creado.
    """
    # Validar que la patente no exista (no inhabilitada)
    patente = kwargs.get("patente")
    if patente:
        existe = db.session.query(Vehiculo).filter_by(patente=patente).first()
        if existe:
            raise ValueError("Ya existe un vehículo con esa patente.")
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

def update_estado_vehiculo(vehiculo_id, en_mantenimiento):
    """
    Actualiza el estado de un vehiculo, indicando si está en mantenimiento o no.

    :param vehiculo_id: ID del vehiculo a actualizar.
    :param en_mantenimiento: Estado de mantenimiento a establecer.
    :return: El vehiculo actualizado, o None si no existe.
    """
    vehiculo = get_vehiculo_by_id(vehiculo_id)
    if vehiculo:
        vehiculo.en_mantenimiento = en_mantenimiento
        db.session.commit()
        return vehiculo
    return None

def delete_vehiculo(vehiculo_id):
    """
    Da de baja lógica a un vehiculo: lo marca como inhabilitado.
    """
    vehiculo = get_vehiculo_by_id(vehiculo_id)
    if vehiculo:
        vehiculo.inhabilitado = True
        db.session.commit()
        return True
    return False

def list_vehiculos(patente=None, incluir_borrados=False):
    """
    Lista todos los vehículos, con opción de filtrar solo los aptos o por patente.
    Excluye los inhabilitados a menos que se solicite incluirlos.
    """
    query = db.session.query(Vehiculo)
    if patente:
        query = query.filter(Vehiculo.patente.ilike(f"%{patente}%"))
    if not incluir_borrados:
        query = query.filter(Vehiculo.inhabilitado == False)
    return query.all()

def list_marcas():
    """
    Lista todas las marcas de vehículos.
    """
    return db.session.query(Vehiculo.marca).distinct().all()

def list_categorias():
    """
    Lista todas las categorías de vehículos.
    """
    return db.session.query(Vehiculo.categoria).distinct().all()

def list_asientos():
    """
    Lista todas las configuraciones de asientos de vehículos.
    """
    return db.session.query(Vehiculo.asientos).distinct().all()