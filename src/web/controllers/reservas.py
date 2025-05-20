from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.core.repositories.reserva import create_reserva, list_reservas_by_user
from src.web.helpers.auth import has_permission

bp = Blueprint("reservas", __name__, url_prefix="/reservas")

@bp.route("/")
@has_permission("reserva_index")
def index():
    reservas = list_reservas_by_user()
    return render_template("reservas/index.html", reservas=reservas)

@bp.route("/show/<int:id>")
@has_permission("reserva_show")
def show(id):
    reserva = list_reservas_by_user(id)
    return render_template("reservas/show.html", reserva=reserva)

@bp.route("/delete/<int:id>")
@has_permission("reserva_delete")
def delete(id):
    reservas = list_reservas_by_user(id)
    if not reservas:
        flash("No se encontró la reserva.", "error")
    flash("Reserva eliminada exitosamente.", "success")
    return redirect(url_for("reservas.index"))
