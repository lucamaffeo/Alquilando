from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.repositories.reserva import create_reserva, list_reservas_by_user

bp = Blueprint("reservas", __name__, url_prefix="/reservas")

@bp.route("/")
def index():
    reservas = list_reservas_by_user()
    return render_template("reservas/index.html", reservas=reservas)

@bp.route("/create", methods=["POST"])
def create():
    data = request.form
    create_reserva(**data)
    flash("Reserva creada exitosamente.", "success")
    return redirect(url_for("reservas.index"))
