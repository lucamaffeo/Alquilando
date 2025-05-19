from src.core.database import db
from src.core.models.permission import Permission

def create_permission(**kwargs):
    """
    Crea un nuevo permiso en la base de datos.

    :param kwargs: Argumentos para crear un nuevo permiso.
    :return: El permiso creado.
    """
    permission = Permission(**kwargs)
    db.session.add(permission)
    db.session.commit()

    return permission
