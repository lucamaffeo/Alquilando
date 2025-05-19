from src.core.database import db

class Sucursal(db.Model):
    __tablename__ = "sucursales"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    ubicacion = db.Column(db.String(255), nullable=False)
    vehiculos = db.relationship('Vehiculo', backref='sucursal', lazy=True)
