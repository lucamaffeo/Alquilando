from sqlalchemy import and_, exists
from werkzeug.security import generate_password_hash
from src.core.database import db
from src.core.models.rol import Role
from src.core.models.user import User
from src.core.models.permission import Permission
from datetime import datetime, date


def list_users():
    return User.query.all()


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def create_user(**kwargs):
    # Validación de email único
    if 'email' in kwargs and User.query.filter_by(email=kwargs['email']).first():
        raise ValueError("El email ya está registrado.")

    # Validación de contraseña
    if 'password' in kwargs and len(kwargs['password']) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres.")

    # Validación de edad mayor a 18 años
    if 'fecha_nacimiento' in kwargs:
        try:
            if isinstance(kwargs['fecha_nacimiento'], str):
                fecha_nac = datetime.strptime(kwargs['fecha_nacimiento'], "%Y-%m-%d").date()
            else:
                fecha_nac = kwargs['fecha_nacimiento']
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            if edad < 18:
                raise ValueError("Debes ser mayor de 18 años para registrarte.")
        except Exception:
            raise ValueError("Fecha de nacimiento inválida. Formato esperado: YYYY-MM-DD.")

    if 'password' in kwargs:
        kwargs['password'] = generate_password_hash(kwargs['password'])
    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user_id, **kwargs):
    user = User.query.get(user_id)
    if not user:
        return False

    if 'password' in kwargs and kwargs['password']:
        kwargs['password'] = generate_password_hash(kwargs['password'])

    for key, value in kwargs.items():
        setattr(user, key, value)

    db.session.commit()
    return True


def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False

    if user.role.name == 'administrador':
        other_admin = User.query.join(Role).filter(
            and_(Role.name == 'administrador', User.id != user_id, User.active == True)
        ).first()
        if not other_admin:
            return False

    db.session.delete(user)
    db.session.commit()
    return True


def has_permission(user_id, permission_name):
    return db.session.query(exists().where(
        and_(
            User.id == user_id,
            User.role_id == Role.id,
            Role.permissions.any(Permission.nombre == permission_name)  # Cambiado a .nombre
        )
    )).scalar()


def list_users_by_role(role_id):
    return User.query.filter_by(role_id=role_id).all()


