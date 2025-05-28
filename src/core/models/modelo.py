from src.core.database import db

class Modelo(db.Model):
    __tablename__ = "modelos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.nombre
