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
    patente = request.args.get("patente", "").strip()
    mensaje = None
    if patente:
        vehiculos_list = vehiculo.list_vehiculos(patente=patente)
        if not vehiculos_list:
            mensaje = f"No existe un vehículo con la patente '{patente}'."
    else:
        vehiculos_list = vehiculo.list_vehiculos()
    return render_template("vehiculos/index.html", vehiculos=vehiculos_list, patente=patente, mensaje=mensaje)

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
        politica_cancelacion = data.get("politica_cancelacion", "Sin reembolso")
        # Validar política de cancelación
        if politica_cancelacion not in ["100% de reembolso", "20% de reembolso", "Sin reembolso"]:
            flash("Política de cancelación inválida.", "error")
            return render_template("vehiculos/register.html", vehiculo=v, is_update=bool(v), sucursales=sucursales)
        from src.core.models.modelo import Modelo
        from src.core.database import db
        modelo_obj = Modelo.query.filter_by(nombre=modelo_nombre, politica_cancelacion=politica_cancelacion).first()
        if not modelo_obj:
            modelo_obj = Modelo(nombre=modelo_nombre, politica_cancelacion=politica_cancelacion)
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
    marca_vehiculos=vehiculo.list_marcas()
    categoria_vehiculos = vehiculo.list_categorias()
    asientos_vehiculos = vehiculo.list_asientos()
    disponibles = []
    for v in vehiculos_sucursal:
        if v.sucursal_id != int(sucursal_id):
            continue
        if v.en_mantenimiento:
            continue
        reservas = reserva.get_reservas_by_vehiculo(v.id)
        disponible = True
        for r in reservas:
            # Solo considerar reservas activas
            if r.estado != "activa":
                continue
            # Si hay cruce de fechas, no está disponible
            if not (fecha_fin_dt < r.fecha_inicio or fecha_inicio_dt > r.fecha_fin):
                disponible = False
                break
        if disponible:
            disponibles.append(v)
      # Filtros opcionales
    filtro_marca = request.form.get("marca")
    filtro_asientos = request.form.get("asientos")
    filtro_categoria = request.form.get("categoria")
     # 🔎 Aplicar los filtros opcionales
    filtrados = []
    for v in disponibles:
        if filtro_marca and v.marca != filtro_marca:
            continue
        if filtro_asientos and str(v.asientos) != filtro_asientos:
            continue
        if filtro_categoria and v.categoria != filtro_categoria:
            continue
        filtrados.append(v)
    # Agrupar por modelo (después de aplicar filtros)
    modelos = {}
    for v in filtrados:
        key = v.modelo_id
        if key not in modelos:
            modelos[key] = {"vehiculos": []}
        modelos[key]["vehiculos"].append(v)
    # Elegir uno al azar por modelo
    modelos_azar = []
    for key, datos in modelos.items():
        vehiculo_azar = random.choice(datos["vehiculos"])
        # Obtener el nombre del modelo
        modelo_nombre = ""
        try:
            modelo_obj = Modelo.query.get(vehiculo_azar.modelo_id)
            if modelo_obj:
                modelo_nombre = modelo_obj.nombre
        except Exception:
            modelo_nombre = str(vehiculo_azar.modelo_id)
        modelos_azar.append({
            "modelo": vehiculo_azar.modelo_id,
            "modelo_nombre": modelo_nombre,
            "vehiculo": vehiculo_azar,
            "precio": vehiculo_azar.precio,
            "marca": vehiculo_azar.marca,
            "categoria": vehiculo_azar.categoria,
            "asientos": vehiculo_azar.asientos,
            "imagen": vehiculo_azar.imagen
        })
    return render_template(
        "vehiculos/disponibles.html",
        modelos=modelos_azar,
        fecha_inicio=fecha_inicio_dt,
        fecha_fin=fecha_fin_dt,
        filtro_marca=filtro_marca,
        filtro_asientos=filtro_asientos,
        filtro_categoria=filtro_categoria,
        marca_vehiculos=marca_vehiculos,
        categoria_vehiculos=categoria_vehiculos,
        asientos_vehiculos=asientos_vehiculos
    )

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
    from flask import request
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    precio_total = None
    precio_por_dia = None
    dias = None
    if fecha_inicio and fecha_fin and v:
        from datetime import datetime
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            dias = (fecha_fin_dt - fecha_inicio_dt).days + 1
            precio_total = int(v.precio) * dias
            precio_por_dia = int(v.precio)
        except Exception:
            precio_total = v.precio
            precio_por_dia = v.precio
    return render_template(
        "vehiculos/show_reserva.html",
        vehiculo=v,
        precio_total=precio_total,
        precio_por_dia=precio_por_dia,
        dias=dias,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


