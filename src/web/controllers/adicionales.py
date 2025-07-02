from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.models.adicional import Adicional
from src.web.helpers.auth import has_permission
from src.core.database import db

bp = Blueprint("adicionales", __name__, url_prefix="/adicionales")

@bp.route("/", methods=["GET"])
@has_permission("adicional_index")
def index():
    adicionales = Adicional.query.all()  # Mostrar todos, sin filtrar por estado
    return render_template("adicionales/index.html", adicionales=adicionales)

@bp.route("/register", methods=["GET", "POST"])
@has_permission("adicional_create")
def register():
    adicional = None
    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        if not nombre or not precio:
            flash("Todos los campos son obligatorios.", "error")
            return render_template("adicionales/register.html", adicional=adicional, is_update=False)
        # Validar nombre único
        existente = Adicional.query.filter_by(nombre=nombre).first()
        if existente:
            flash("Ya existe un adicional con ese nombre.", "error")
            return render_template("adicionales/register.html", adicional=adicional, is_update=False)
        adicional = Adicional(nombre=nombre, precio=float(precio), estado="activo")
        db.session.add(adicional)
        db.session.commit()
        flash("Adicional registrado exitosamente.", "success")
        return redirect(url_for("adicionales.index"))
    return render_template("adicionales/register.html", adicional=adicional, is_update=False)

@bp.route("/actualizar/<int:id>", methods=["GET", "POST"])
@has_permission("adicional_update")
def actualizar(id):
    adicional = Adicional.query.get(id)
    if not adicional:
        flash("Adicional no encontrado.", "error")
        return redirect(url_for("adicionales.index"))
    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        if not nombre or not precio:
            flash("Todos los campos son obligatorios.", "error")
            return render_template("adicionales/register.html", adicional=adicional, is_update=True)
        # Validar nombre único (excepto el propio)
        existente = Adicional.query.filter(Adicional.nombre == nombre, Adicional.id != id).first()
        if existente:
            flash("Ya existe un adicional con ese nombre.", "error")
            return render_template("adicionales/register.html", adicional=adicional, is_update=True)
        adicional.nombre = nombre
        adicional.precio = float(precio)
        db.session.commit()
        flash("Adicional actualizado exitosamente.", "success")
        return redirect(url_for("adicionales.index"))
    return render_template("adicionales/register.html", adicional=adicional, is_update=True)

@bp.route("/eliminar/<int:id>", methods=["POST"])
@has_permission("adicional_delete")
def eliminar(id):
    adicional = Adicional.query.get(id)
    if not adicional:
        flash("Adicional no encontrado.", "error")
        return redirect(url_for("adicionales.index"))
    adicional.estado = "eliminado"  # Baja lógica
    db.session.commit()
    flash("Adicional eliminado exitosamente.", "success")
    return redirect(url_for("adicionales.index"))

@bp.route("/habilitar/<int:id>", methods=["POST"])
@has_permission("adicional_update")
def habilitar(id):
    adicional = Adicional.query.get(id)
    if not adicional:
        flash("Adicional no encontrado.", "error")
        return redirect(url_for("adicionales.index"))
    adicional.estado = "activo"
    db.session.commit()
    flash("Adicional habilitado exitosamente.", "success")
    return redirect(url_for("adicionales.index"))


