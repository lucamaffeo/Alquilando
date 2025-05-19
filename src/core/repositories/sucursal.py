from src.core.database import db
from src.core.models.sucursal import Sucursal

def list_sucursales():
    """
    Lista todas las sucursales.
    """
    return Sucursal.query.all()

def get_sucursal_by_id(sucursal_id):
    """
    Obtiene una sucursal por su ID.
    """
    return Sucursal.query.get(sucursal_id)

def create_sucursal(**kwargs):
    """
    Crea una nueva sucursal.
    """
    sucursal = Sucursal(**kwargs)
    db.session.add(sucursal)
    db.session.commit()
    return sucursal

def update_sucursal(sucursal_id, **kwargs):
    """
    Actualiza una sucursal existente.
    """
    sucursal = get_sucursal_by_id(sucursal_id)
    if sucursal:
        for key, value in kwargs.items():
            setattr(sucursal, key, value)
        db.session.commit()
        return sucursal
    return None

def delete_sucursal(sucursal_id):
    """
    Elimina una sucursal por su ID.
    """
    sucursal = get_sucursal_by_id(sucursal_id)
    if sucursal:
        db.session.delete(sucursal)
        db.session.commit()
        return True
    return False
