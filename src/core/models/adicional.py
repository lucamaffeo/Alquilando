from src.core.database import db

reserva_adicional = db.Table(
    "reserva_adicional",
    db.Column("reserva_id", db.Integer, db.ForeignKey("reservas.id"), primary_key=True),
    db.Column("adicional_id", db.Integer, db.ForeignKey("adicionales.id"), primary_key=True)
)

class Adicional(db.Model):
    __tablename__ = "adicionales"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="activo")  # Nuevo campo
