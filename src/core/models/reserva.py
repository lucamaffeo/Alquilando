from src.core.database import db
from src.core.models.adicional import reserva_adicional

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), default="activa")
    precio_total_vehiculo = db.Column(db.Float, nullable=False)  # Nuevo campo

    vehiculo = db.relationship("Vehiculo", backref="reservas")
    user = db.relationship("User", backref="reservas")
    adicionales = db.relationship(
        "Adicional",
        secondary=reserva_adicional,
        backref="reservas"
    )
