from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core.repositories.reserva import create_reserva, list_reservas_by_user
from src.core.repositories import vehiculo
from src.web.helpers.auth import has_permission
from datetime import datetime

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

@bp.route("/pago", methods=["GET", "POST"])
def pago():
    if not session.get("user_id"):
        flash("Debes iniciar sesión o registrarte para reservar.", "error")
        return redirect(url_for("usuarios.register"))
    if request.method == "POST":
        vehiculo_id = request.form.get("vehiculo_id")
        fecha_inicio = request.form.get("fecha_inicio")
        fecha_fin = request.form.get("fecha_fin")
    else:
        vehiculo_id = request.args.get("vehiculo_id")
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")
    v = vehiculo.get_vehiculo_by_id(vehiculo_id)
    # Calcular precio total
    precio_total = None
    if v and fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            dias = (fecha_fin_dt - fecha_inicio_dt).days + 1
            precio_total = int(v.precio) * dias
        except Exception:
            precio_total = v.precio
    if request.method == "POST":
        # Aquí iría la lógica de pago y creación de reserva
        flash("Pago realizado y reserva confirmada.", "success")
        return redirect(url_for("reservas.index"))
    return render_template(
        "reservas/pago.html",
        vehiculo=v,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        precio_total=precio_total
    )
