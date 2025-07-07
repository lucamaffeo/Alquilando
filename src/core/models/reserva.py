from src.core.database import db
from src.core.models.adicional import reserva_adicional

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    vehiculo_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=False)
    vehiculo_asignado_id = db.Column(db.Integer, db.ForeignKey("vehiculos.id"), nullable=True)  # Nuevo campo
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(50), default="activa")
    precio_total_vehiculo = db.Column(db.Float, nullable=False)  # Nuevo campo
    calificacion = db.Column(db.Integer, nullable=True)
    comentario = db.Column(db.String(255), nullable=True)
    precio_total_adicionales = db.Column(db.Float, default=0.0)  # Nuevo campo para el total de adicionales
    reporte_devolucion = db.Column(db.String(255), nullable=True)  # Nuevo campo para el reporte de devolución
    fecha_cancelacion = db.Column(db.Date, nullable=True)  # Nueva columna para la fecha de cancelación

    vehiculo = db.relationship("Vehiculo", foreign_keys=[vehiculo_id], backref="reservas")
    vehiculo_asignado = db.relationship("Vehiculo", foreign_keys=[vehiculo_asignado_id], backref="reservas_asignadas")
    user = db.relationship("User", backref="reservas")
    adicionales = db.relationship(
        "Adicional",
        secondary=reserva_adicional,
        backref="reservas"
    )
