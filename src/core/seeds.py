from src.core.database import db
from src.core.repositories.rol import create_role
from src.core.repositories.user import create_user
from src.core.repositories.permission import create_permission 
from src.core.repositories.vehiculo import create_vehiculo
from src.core.repositories.sucursal import create_sucursal
from src.core.repositories.reserva import create_reserva

def run():
    # Crear permisos de usuarios
    user_index = create_permission(nombre="user_index")
    user_show = create_permission(nombre="user_show")
    user_update = create_permission(nombre="user_update")
    user_delete = create_permission(nombre="user_delete")
    user_create_presencial = create_permission(nombre="user_create_presencial")
    
    # Permisos de sucursal
    sucursal_index = create_permission(nombre="sucursal_index")
    sucursal_show = create_permission(nombre="sucursal_show")
    sucursal_create = create_permission(nombre="sucursal_create")

    # Crear permisos de vehículos
    vehicle_index = create_permission(nombre="vehicle_index")
    vehicle_show = create_permission(nombre="vehicle_show")
    vehicle_create = create_permission(nombre="vehicle_create")
    vehicle_update = create_permission(nombre="vehicle_update")
    vehicle_delete = create_permission(nombre="vehicle_delete")
    vehicle_cambiar_estado = create_permission(nombre="vehicle_cambiar_estado")

    #crear permisos reservas
    reserva_index = create_permission(nombre="reserva_index")
    reserva_show = create_permission(nombre="reserva_show")
    reserva_delete = create_permission(nombre="reserva_delete")

    # Crear permisos de empleados
    employee_create = create_permission(nombre="employee_create")

    # Crear roles
    admin_role = create_role(name="admin", permissions=[
        user_index, user_show, user_update, user_delete,
        vehicle_create, vehicle_update, vehicle_delete, vehicle_show, vehicle_index,
        sucursal_index, sucursal_show, sucursal_create, employee_create
    ])
    usuario_role = create_role(name="usuario registrado", permissions=[
        user_show, user_update, reserva_index, reserva_show, reserva_delete,
    ])
    empleado_role = create_role(name="empleado", permissions=[
    vehicle_show, vehicle_index, vehicle_cambiar_estado, user_update, user_create_presencial,
    ])

    # Crear usuarios

    admin3 = create_user(
        nombre="admin3",
        email="ale.proia@hotmail.com",
        password="admin123",  # Cambiado a 8 caracteres
        role_id=1,
        apellido="Proia",
        telefono="123456789",
        dni="77777777",
        fecha_nacimiento="2000-01-01",
    )
    admin4 = create_user(
        nombre="admin4",
        email="guillehelfer@gmail.com",
        password="admin123",  # Cambiado a 8 caracteres
        role_id=1,
        apellido="Helfer",
        telefono="123346568",
        dni="45034325",
        fecha_nacimiento="2000-01-01",
    )
    admin2 = create_user(
        nombre="admin2",
        email="diamondcodedev@gmail.com",
        password="admin123",  # Cambiado a 8 caracteres
        role_id=1,
        apellido="Helfer",
        telefono="123456789",
        dni="44444444",
        fecha_nacimiento="2001-01-01",
    )
    admin = create_user(
        nombre="Luca",
        email="lucamaffeo@gmail.com",
        password="admin123",  # Cambiado a 8 caracteres
        role_id=1,
        apellido="Maffeo",
        telefono="123456789",
        dni="40882818",
        fecha_nacimiento="2000-01-01",
    )
    admin = create_user(
        nombre="Luca",
        email="diplacidofelipe@gmail.com",
        password="admin123",  # Cambiado a 8 caracteres
        role_id=1,
        apellido="Maffeo",
        telefono="123456789",
        dni="12345679",
        fecha_nacimiento="2000-01-01",
    )
    empleado = create_user(
        nombre="empleado",
        email="empleado@empleado.com",
        password="empleado123",  # Cambiado a más de 6 caracteres
        role_id=3,
        apellido="Proia",
        telefono="123456789",
        dni="55555555",
        fecha_nacimiento="2000-01-01",
    )
    user = create_user(
        nombre="usuario",
        email="user@user.com",
        password="123456",  # Cambiado a más de 6 caracteres
        role_id=2,
        apellido="Helfer",
        telefono="123456789",  
        dni="66666666",
        fecha_nacimiento="2000-01-01",  
    )

    # Crear sucursales
    sucursal1 = create_sucursal(
        nombre="Sucursal Centro",
        ubicacion="Av. Corrientes 1234",
    )
    sucursal2 = create_sucursal(
        nombre="Sucursal Norte",
        ubicacion="Av. Libertador 5678",
    )

    sucursal3 = create_sucursal(
        nombre="Sucursal Sur",
        ubicacion="Av. Rivadavia 91011",
    )

    # Crear modelos (si no existen)
    from src.core.models.modelo import Modelo

    def get_or_create_modelo(nombre, politica_cancelacion):
        modelo = Modelo.query.filter_by(nombre=nombre, politica_cancelacion=politica_cancelacion).first()
        if not modelo:
            modelo = Modelo(nombre=nombre, politica_cancelacion=politica_cancelacion)
            db.session.add(modelo)
            db.session.commit()
        return modelo

   
    # Crear vehículos para ambas sucursales
    # Sucursal 1
    # crear modelo


    

    # Sucursal 2 (solo autos con imágenes disponibles)
    create_vehiculo(
        patente="ABC456",
        modelo_id=get_or_create_modelo("Corolla", "100% de reembolso").id,
        marca="Toyota",
        categoria="Sedan",
        asientos=5,
        precio=20000,
        anio=2020,
        sucursal_id=sucursal2.id,
        imagen="Toyota_Corolla.png"
    )
    create_vehiculo(
        patente="ZZZ949",
        modelo_id=get_or_create_modelo("Corolla", "100% de reembolso").id,
        marca="Toyota",
        categoria="Sedan",
        asientos=5,
        precio=20000,
        anio=2019,
        sucursal_id=sucursal2.id,
        imagen="Toyota_Corolla.png"
    )
    create_vehiculo(
        patente="SUV555",
        modelo_id=get_or_create_modelo("CR-V", "100% de reembolso").id,
        marca="Honda",
        categoria="SUV",
        asientos=7,
        precio=30000,
        anio=2022,
        sucursal_id=sucursal2.id,
        imagen="Honda_CRV.jpg"
    )
    create_vehiculo(
        patente="PKP444",
        modelo_id=get_or_create_modelo("Amarok", "Sin reembolso").id,
        marca="Volkswagen",
        categoria="Pickup",
        asientos=5,
        precio=35000,   
        anio=2022,
        sucursal_id=sucursal2.id,
        imagen="Volkswagen_Amarok.png"
    )
    create_vehiculo(
        patente="FOC111",
        modelo_id=get_or_create_modelo("Focus", "20% de reembolso").id,
        marca="Ford",
        categoria="Hatchback",
        asientos=5,
        precio=18000,
        anio=2018,
        sucursal_id=sucursal2.id,
        imagen="Ford_Focus.png"
    )
    create_vehiculo(
        patente="RAN222",
        modelo_id=get_or_create_modelo("Ranger", "20% de reembolso").id,
        marca="Ford",
        categoria="Pickup",
        asientos=5,
        precio=32000,
        anio=2021,
        sucursal_id=sucursal2.id,
        imagen="Ford_Ranger.png"
    )
    create_vehiculo(
        patente="FLU333",
        modelo_id=get_or_create_modelo("Fluence", "100% de reembolso").id,
        marca="Renault",
        categoria="Sedan",
        asientos=5,
        precio=21000,
        anio=2020,
        sucursal_id=sucursal2.id,
        imagen="Renault_Fluence.png"
    )
    create_vehiculo(
        patente="HIL444",
        modelo_id=get_or_create_modelo("Hilux", "20% de reembolso").id,
        marca="Toyota",
        categoria="Pickup",
        asientos=5,
        precio=34000,
        anio=2022,
        sucursal_id=sucursal2.id,
        imagen="Toyota_Hillux.png"
    )
    create_vehiculo(
        patente="SWJ555",
        modelo_id=get_or_create_modelo("SW4", "100% de reembolso").id,
        marca="Toyota",
        categoria="SUV",
        asientos=7,
        precio=37000,
        anio=2023,
        sucursal_id=sucursal2.id,
        imagen="Toyota_Sw4.jpg"
    )
    create_vehiculo(
        patente="AUD888",
        modelo_id=get_or_create_modelo("A3", "Sin reembolso").id,
        marca="Audi",
        categoria="Coupe",
        asientos=2,
        precio=35000,
        anio=2022,
        sucursal_id=sucursal2.id,
        imagen="Audi_A3.png"
    )
    # Reservas
    create_reserva(
        vehiculo_id=5,  # ID del vehículo que se va a reservar
        user_id=user.id,  # ID del usuario que realiza la reserva
        fecha_inicio="2023-10-01",
        fecha_fin="2023-10-05",
        estado="finalizada"
    )

    # --- Reservas adicionales para user@user.com ---
    
    create_reserva(
        vehiculo_id=1,
        user_id=user.id,
        fecha_inicio="2023-09-01",
        fecha_fin="2023-09-05",
        estado="finalizada"
    )
    # 2 canceladas
    create_reserva(
        vehiculo_id=4,
        user_id=user.id,
        fecha_inicio="2023-06-01",
        fecha_fin="2023-06-05",
        estado="cancelada"
    )
    create_reserva(
        vehiculo_id=2,
        user_id=user.id,
        fecha_inicio="2023-05-10",
        fecha_fin="2023-05-15",
        estado="cancelada"
    )
    # 2 activas (misma fecha, diferente vehículo)
    create_reserva(
        vehiculo_id=1,
        user_id=user.id,
        fecha_inicio="2026-12-01",
        fecha_fin="2026-12-10",
        estado="activa"
    )
    create_reserva(
        vehiculo_id=3,
        user_id=user.id,
        fecha_inicio="2026-12-01",
        fecha_fin="2026-12-10",
        estado="activa"
    )

    print("Seed ejecutado correctamente!")
