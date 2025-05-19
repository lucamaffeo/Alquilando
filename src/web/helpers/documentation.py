from functools import wraps
from flask import abort

ALLOWED_ENTITIES = {"horses", "employees", "riders"}


def clean_entity_type(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        entity_type = kwargs.get('entity_type', '').strip().replace(
            " ", "_").replace("%20", "")
        if entity_type not in ALLOWED_ENTITIES:  # Validar entidad permitida
            abort(403)  # Retorna error 403 Forbidden si no tiene permiso
        kwargs['entity_type'] = entity_type
        return f(*args, **kwargs)
    return decorated_function
