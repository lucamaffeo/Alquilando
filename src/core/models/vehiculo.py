from src.core.database import db


class Vehiculo(db.Model):
    __tablename__ = "vehiculos"

    id = db.Column(db.Integer, primary_key=True)
    patente = db.Column(db.String(10), unique=True, nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    modelo_id = db.Column(db.Integer, db.ForeignKey('modelos.id'), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    asientos = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    sucursal_id = db.Column(db.Integer, db.ForeignKey('sucursales.id'), nullable=False)
    en_mantenimiento = db.Column(db.Boolean, default=False, nullable=False)
    imagen = db.Column(db.String(255), nullable=True) 

    modelo_rel = db.relationship("Modelo", backref="vehiculos")

    def modelo_nombre(self):
        return self.modelo_rel.nombre if self.modelo_rel else ""

    def estado(self):
        return "En mantenimiento" if self.en_mantenimiento else "Activo"
