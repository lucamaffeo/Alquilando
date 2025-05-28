from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from src.core.repositories.reserva import create_reserva, list_reservas_by_user
from src.core.repositories import vehiculo
from src.web.helpers.auth import has_permission
from datetime import datetime
from resources.TARJETAS_VALIDAS import tarjetas_credito, tarjetas_debito
import random  

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
    encontre = False
    if not session.get("user_id"):
        flash("Debes iniciar sesión para reservar.", "error")
        return redirect(url_for("usuarios.login"))
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
        # Simular fallo de conexión (10% de probabilidad)
        if random.random() < 0.1:
            flash("Error de conexión al procesar el pago. Por favor, intente nuevamente.", "error")
            return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
        datos_tarjeta = request.form
        tipo_tarjeta = datos_tarjeta.get("tipo_tarjeta")
        numero_tarjeta = datos_tarjeta.get("tarjeta")
        if tipo_tarjeta == "credito":
            for tarjeta in tarjetas_credito:
                if tarjeta["numero"] == numero_tarjeta:
                    encontre = True
                    if tarjeta["titular"].lower() != datos_tarjeta.get("nombre").lower():
                        flash("El titular de la tarjeta no coincide.", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    if tarjeta["vencimiento"] < datetime.now().strftime("%m/%y"):
                        flash("La tarjeta de crédito ha expirado.", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    if tarjeta["codigo_seguridad"] != datos_tarjeta.get("cvv"):
                        flash("Codigo de seguridad incorrecto .", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    if tarjeta["saldo"] < precio_total:
                        flash("La tarjeta no posee credito disponible.", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    break
        if tipo_tarjeta == "debito":       
            for tarjeta in tarjetas_debito:
                if tarjeta["numero"] == numero_tarjeta:
                    encontre = True
                    if tarjeta["titular"].lower() != datos_tarjeta.get("nombre").lower():
                        flash("El titular de la tarjeta no coincide.", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    if tarjeta["vencimiento"] < datetime.now().strftime("%m/%y"):
                        flash("La tarjeta de débito ha expirado.", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    if tarjeta["codigo_seguridad"] != datos_tarjeta.get("cvv"):
                        flash("Codigo de seguridad incorrecto .", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    if tarjeta["saldo"] < precio_total:
                        flash("La tarjeta de debito no posee saldo suficiente.", "error")
                        return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
                    break
        if not encontre:
            flash("Hubo un error por código de tarjeta inexistente", "error")
            return redirect(url_for("reservas.pago", vehiculo_id=vehiculo_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin))
        # Si todo OK, crear la reserva y redirigir a mis reservas
        create_reserva(
            vehiculo_id=vehiculo_id,
            user_id=session.get("user_id"),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )
        flash("Pago realizado y reserva confirmada.", "success")
        return redirect(url_for("reservas.mis_reservas"))
    return render_template(
        "reservas/pago.html",
        vehiculo=v,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        precio_total=precio_total
    )

@bp.route("/mis-reservas")
@has_permission("reserva_index")
def mis_reservas():
    user_id = session.get("user_id")
    user_role = session.get("user_role")
    if not user_id or user_role != "usuario registrado":
        flash("No tienes permiso para ver esta sección.", "error")
        return redirect(url_for("global.inicio_global"))
    reservas = list_reservas_by_user(user_id)
    if not reservas:
        return render_template("reservas/index.html", reservas=reservas)
    return render_template("reservas/index.html", reservas=reservas)
