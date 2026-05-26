from datetime import datetime
from src.core.database import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.String(20), nullable=True)
    nombre = db.Column(db.String(255), nullable=True)
    apellido = db.Column(db.String(255), nullable=True)
    telefono = db.Column(db.String(255), nullable=True)
    fecha_nacimiento = db.Column(db.Date, nullable=True)

    estado = db.Column(db.String(20), default="activo")  # Nuevo campo: 'activo' o 'eliminado'

    inserted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref='users', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "role_id": self.role_id,
            "active": self.active,
            "inserted_at": self.inserted_at,
            "updated_at": self.updated_at,
            "permissions": [p.name for p in self.role.permissions]
        }
