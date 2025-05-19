from functools import wraps
import logging
from flask import session, abort

from src.core.repositories import user as auth

logger = logging.getLogger(__name__)


def is_authenticated(session):
    return session.get("user_id") != None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return abort(401)
        return f(*args, **kwargs)

    return decorated_function


def has_permission(user_id, permission_name):
    user_data = auth.get_user_by_id(user_id)
    if user_data and user_data.role:
        return user_data.role.has_permission(permission_name)
    return False


def has_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_authenticated(session):
                return abort(401)
            user_id = session["user_id"]
            if auth.has_permission(user_id, permission):
                return f(*args, **kwargs)
            return abort(403)
        return decorated_function
    return decorator
