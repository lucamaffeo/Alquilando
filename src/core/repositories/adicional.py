from src.core.models.adicional import Adicional
from src.core.database import db

def list_adicionales():
    return Adicional.query.all()
