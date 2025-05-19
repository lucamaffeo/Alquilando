from sqlalchemy import and_, exists
from werkzeug.security import generate_password_hash
from src.core.database import db
from src.core.models.rol import Role
from src.core.models.user import User
from src.core.models.permission import Permission


def list_users():
    return User.query.all()


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def create_user(**kwargs):
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
            Role.permissions.any(Permission.name == permission_name)
        )
    )).scalar()


def list_users_by_role(role_id):
    return User.query.filter_by(role_id=role_id).all()


