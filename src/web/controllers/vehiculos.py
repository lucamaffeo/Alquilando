from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.core.repositories import vehiculo, sucursal, reserva
from src.web.helpers.auth import has_permission
from datetime import datetime, timedelta
import random
from src.core.models.modelo import Modelo
import os
from werkzeug.utils import secure_filename

bp = Blueprint("vehiculos", __name__, url_prefix="/vehiculos")

@bp.route("/")
@has_permission("vehicle_index")
def index():
    vehiculos_list = vehiculo.list_vehiculos()
    return render_template("vehiculos/index.html", vehiculos=vehiculos_list)

@bp.route("/<int:id>")
@has_permission("vehicle_show")
def show(id):
    v = vehiculo.get_vehiculo_by_id(id)
    return render_template("vehiculos/show.html", vehiculo=v)

@bp.route("/register", methods=["GET", "POST"])
@has_permission("vehicle_create")
def register():
    vehiculo_id = request.args.get("id")
    v = vehiculo.get_vehiculo_by_id(vehiculo_id) if vehiculo_id else None
    sucursales = sucursal.list_sucursales()
    if request.method == "POST":
        data = request.form
        modelo_nombre = data["modelo"].strip()
        from src.core.models.modelo import Modelo
        from src.core.database import db
        modelo_obj = Modelo.query.filter_by(nombre=modelo_nombre).first()
        if not modelo_obj:
            modelo_obj = Modelo(nombre=modelo_nombre)
            db.session.add(modelo_obj)
            db.session.commit()
        modelo_id = modelo_obj.id
        # Manejo de imagen
        imagen_file = request.files.get("imagen")
        imagen_nombre = None
        if imagen_file and imagen_file.filename:
            from werkzeug.utils import secure_filename
            import os
            imagen_nombre = secure_filename(imagen_file.filename)
            ruta = os.path.join("static", "images", imagen_nombre)
            imagen_file.save(ruta)
        elif v:
            imagen_nombre = v.imagen  # Mantener la imagen anterior si no se sube una nueva

        try:
            if v:
                vehiculo.update_vehiculo(
                    v.id,
                    modelo_id=modelo_id,
                    marca=data["marca"],
                    categoria=data["categoria"],
                    asientos=data["asientos"],
                    precio=data["precio"],
                    anio=data["anio"],
                    sucursal_id=int(data["sucursal_id"]),
                    imagen=imagen_nombre,
                    en_mantenimiento=True if data.get("en_mantenimiento") == "on" else False,
                )
                flash("Vehículo actualizado exitosamente.", "success")
            else:
                vehiculo.create_vehiculo(
                    patente=data["patente"],
                    modelo_id=modelo_id,
                    marca=data["marca"],
                    categoria=data["categoria"],
                    asientos=data["asientos"],
                    precio=data["precio"],
                    anio=data["anio"],
                    sucursal_id=int(data["sucursal_id"]),
                    imagen=imagen_nombre,
                    en_mantenimiento=True if data.get("en_mantenimiento") == "on" else False,
                )
                flash("Vehículo creado exitosamente.", "success")
            return redirect(url_for("vehiculos.index"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("vehiculos/register.html", vehiculo=v, is_update=bool(v), sucursales=sucursales)

@bp.route("/cambiar_estado/<int:id>", methods=["POST"])
@has_permission("vehicle_cambiar_estado")
def cambiar_estado(id):
    v = vehiculo.get_vehiculo_by_id(id)
    if not v:
        flash("Vehículo no encontrado.", "error")
        return redirect(url_for("vehiculos.index"))
    nuevo_estado = not v.en_mantenimiento
    vehiculo.update_estado_vehiculo(id, nuevo_estado)
    if nuevo_estado:
        flash("El vehículo fue puesto en mantenimiento.", "success")
    else:
        flash("El vehículo está activo.", "success")
    return redirect(url_for("vehiculos.show", id=id))

@bp.route("/delete/<int:id>", methods=["POST"])
@has_permission("vehicle_delete")
def delete(id):
    try:
        vehiculo.delete_vehiculo(id)    
        flash("Vehículo eliminado exitosamente.", "success")
    except ValueError as e:
        flash(str(e), "error")
    return redirect(url_for("vehiculos.index"))

@bp.route("/disponibles", methods=["POST"])
def disponibles():
    fecha_inicio = request.form.get("fecha_inicio")
    fecha_fin = request.form.get("fecha_fin")
    sucursal_id = request.form.get("sucursal")
    if not (fecha_inicio and fecha_fin and sucursal_id):
        flash("Debe completar todos los campos.", "error")
        return redirect(url_for("global.inicio_global"))
    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    hoy = datetime.now().date()
    if fecha_inicio_dt <= hoy:
        flash("La fecha de inicio debe ser a partir de mañana.", "error")
        return redirect(url_for("global.inicio_global"))
    if fecha_fin_dt < fecha_inicio_dt:
        flash("La fecha fin no puede ser menor a la fecha inicio.", "error")
        return redirect(url_for("global.inicio_global"))
    vehiculos_sucursal = vehiculo.list_vehiculos()
    disponibles = []
    for v in vehiculos_sucursal:
        if v.sucursal_id != int(sucursal_id):
            continue
        if v.en_mantenimiento:
            continue
        reservas = reserva.get_reservas_by_vehiculo(v.id)
        disponible = True
        for r in reservas:
            # Si hay cruce de fechas, no está disponible
            if not (fecha_fin_dt < r.fecha_inicio or fecha_inicio_dt > r.fecha_fin):
                disponible = False
                break
        if disponible:
            disponibles.append(v)
    # Agrupar por modelo (string)
    modelos = {}
    for v in disponibles:
        key = v.modelo
        if key not in modelos:
            modelos[key] = {"vehiculos": []}
        modelos[key]["vehiculos"].append(v)
    # Elegir uno al azar por modelo
    modelos_azar = []
    for key, datos in modelos.items():
        vehiculo_azar = random.choice(datos["vehiculos"])
        modelos_azar.append({
            "modelo": vehiculo_azar.modelo,
            "vehiculo": vehiculo_azar,
            "precio": vehiculo_azar.precio,
            "marca": vehiculo_azar.marca,
            "categoria": vehiculo_azar.categoria,
            "asientos": vehiculo_azar.asientos,
            "imagen": vehiculo_azar.imagen
        })
    return render_template("vehiculos/disponibles.html", modelos=modelos_azar, fecha_inicio=fecha_inicio_dt, fecha_fin=fecha_fin_dt)

@bp.route("/categorias")
def categorias():
    autos = vehiculo.list_vehiculos()
    categorias = {}
    for auto in autos:
        if auto.categoria not in categorias:
            categorias[auto.categoria] = {"asientos": auto.asientos, "vehiculos": []}
        categorias[auto.categoria]["vehiculos"].append(auto)
    return render_template("vehiculos/categorias.html", categorias=categorias)

@bp.route("/show_reserva/<int:id>")
def show_reserva(id):
    v = vehiculo.get_vehiculo_by_id(id)
    return render_template("vehiculos/show_reserva.html", vehiculo=v)


