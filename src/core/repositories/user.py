from sqlalchemy import and_, exists
from werkzeug.security import generate_password_hash
from src.core.database import db
from src.core.models.rol import Role
from src.core.models.user import User
from src.core.models.permission import Permission
from datetime import datetime, date
from sqlalchemy import cast, String


def list_users(dni=None):
    """
    Lista todos los usuarios, con opción de filtrar solo por dni.
    """
    query = db.session.query(User)
    if dni:
        query = query.filter(cast(User.dni, String).ilike(f"%{dni}%"))
    return query.all()


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def create_user(**kwargs):
    # Validación de email único
    if 'email' in kwargs and User.query.filter_by(email=kwargs['email']).first():
        raise ValueError("El email ya está registrado.")

    if 'dni' in kwargs and User.query.filter_by(dni=kwargs['dni']).first():
        raise ValueError("El DNI ya está registrado.")
    
    #valida q el dni tenga entre 7 y 8 caracteres
    if 'dni' in kwargs and (len(kwargs['dni']) < 7 or len(kwargs['dni']) > 8):
        raise ValueError("El DNI debe tener entre 7 y 8 caracteres.")
    
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
            raise ValueError("Debes ser mayor de 18 años para registrarte.")

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

    # Solo actualizar la contraseña si se ingresa una nueva y no es vacía
    password = kwargs.pop('password', None)
    if password is not None and password != "":
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        user.password = generate_password_hash(password)
    # Si password es None o vacío, no modificar el campo

    for key, value in kwargs.items():
        setattr(user, key, value)

    db.session.commit()
    return True


def delete_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        user.estado = "eliminado"
        from src.core.database import db
        db.session.commit()
        return True
    return False


def has_permission(user_id, permission_name):
    return db.session.query(exists().where(
        and_(
            User.id == user_id,
            User.role_id == Role.id,
            Role.permissions.any(Permission.nombre == permission_name)
        )
    )).scalar()

def list_users_by_role(role_id):
    return User.query.filter_by(role_id=role_id).all()
    


def list_users_by_role(role_id):
    return User.query.filter_by(role_id=role_id).all()


