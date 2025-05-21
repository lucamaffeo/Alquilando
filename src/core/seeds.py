from src.core.database import db
from src.core.repositories.rol import create_role
from src.core.repositories.user import create_user
from src.core.repositories.permission import create_permission 
from src.core.repositories.vehiculo import create_vehiculo
from src.core.repositories.sucursal import create_sucursal

def run():
    # Crear permisos de usuarios
    user_index = create_permission(nombre="user_index")
    user_show = create_permission(nombre="user_show")
    user_update = create_permission(nombre="user_update")
    user_delete = create_permission(nombre="user_delete")

    # Crear permisos de vehículos
    vehicle_index = create_permission(nombre="vehicle_index")
    vehicle_show = create_permission(nombre="vehicle_show")
    vehicle_create = create_permission(nombre="vehicle_create")
    vehicle_update = create_permission(nombre="vehicle_update")
    vehicle_delete = create_permission(nombre="vehicle_delete")

    #crear permisos reservas
    reserva_index = create_permission(nombre="reserva_index")
    reserva_show = create_permission(nombre="reserva_show")
    reserva_delete = create_permission(nombre="reserva_delete")

    # Crear roles
    admin_role = create_role(name="admin", permissions=[
        user_index, user_show, user_update, user_delete,
        vehicle_create, vehicle_update, vehicle_delete, vehicle_show, vehicle_index
    ])
    usuario_role = create_role(name="usuario registrado", permissions=[
        user_show, user_update, reserva_index, reserva_show, reserva_delete,
    ])
    empleado_role = create_role(name="empleado", permissions=[
    vehicle_show, vehicle_index
    ])

    # Crear usuarios
    admin = create_user(
        nombre="admin",
        email="admin@admin.com",
        password="admin123",  # Cambiado a 8 caracteres
        role_id=1,
        apellido="Maffeo",
        telefono="123456789",
        dni="12345678",
        fecha_nacimiento="2000-01-01",
    )
    empleado = create_user(
        nombre="empleado",
        email="empleado@empleado.com",
        password="empleado123",  # Cambiado a más de 6 caracteres
        role_id=3,
        apellido="Proia",
        telefono="123456789",
        dni="12345678",
        fecha_nacimiento="2000-01-01",
    )
    usuario_registrado = create_user(
        nombre="usuario_registrado",
        email="user@user.com",
        password="123456",
        role_id=2,
        apellido="Di placido",
        telefono="123456789",
        dni="12345678",
        fecha_nacimiento="2000-01-01",
    )
    usuario_registrado2 = create_user(
        nombre="usuario_registrado2",
        email="user2@user.com",
        password="123456",
        role_id=2,
        apellido="Helfer",
        telefono="123456789",
        dni="12345678",
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

    # Crear vehículos para ambas sucursales
    # Sucursal 1
    create_vehiculo(
        marca="Toyota", modelo="Corolla", anio=2020, patente="ABC123", precio=20000,
        sucursal_id=sucursal1.id, categoria="Sedan", asientos=5
    )
    create_vehiculo(
        marca="Ford", modelo="Focus", anio=2019, patente="DEF456", precio=18000,
        sucursal_id=sucursal1.id, categoria="Sedan", asientos=5
    )
    create_vehiculo(
        marca="Renault", modelo="Fluence", anio=2021, patente="SED111", precio=21000,
        sucursal_id=sucursal1.id, categoria="Sedan", asientos=5
    )
    create_vehiculo(
        marca="Chevrolet", modelo="Tracker", anio=2021, patente="SUV111", precio=25000,
        sucursal_id=sucursal1.id, categoria="SUV", asientos=7
    )
    create_vehiculo(
        marca="Honda", modelo="CR-V", anio=2022, patente="SUV222", precio=30000,
        sucursal_id=sucursal1.id, categoria="SUV", asientos=7
    )
    create_vehiculo(
        marca="Toyota", modelo="SW4", anio=2023, patente="SUV333", precio=35000,
        sucursal_id=sucursal1.id, categoria="SUV", asientos=7
    )
    create_vehiculo(
        marca="Volkswagen", modelo="Amarok", anio=2022, patente="PKP111", precio=35000,
        sucursal_id=sucursal1.id, categoria="Pickup", asientos=5
    )
    create_vehiculo(
        marca="Ford", modelo="Ranger", anio=2021, patente="PKP222", precio=34000,
        sucursal_id=sucursal1.id, categoria="Pickup", asientos=5
    )
    create_vehiculo(
        marca="Toyota", modelo="Hilux", anio=2023, patente="PKP333", precio=36000,
        sucursal_id=sucursal1.id, categoria="Pickup", asientos=5
    )

    # Sucursal 2
    create_vehiculo(
        marca="Toyota", modelo="Corolla", anio=2020, patente="ABC456", precio=20000,
        sucursal_id=sucursal2.id, categoria="Sedan", asientos=5
    )
    create_vehiculo(
        marca="Ford", modelo="Focus", anio=2019, patente="DEF789", precio=18000,
        sucursal_id=sucursal2.id, categoria="Sedan", asientos=5
    )
    create_vehiculo(
        marca="Renault", modelo="Fluence", anio=2021, patente="SED222", precio=21000,
        sucursal_id=sucursal2.id, categoria="Sedan", asientos=5
    )
    create_vehiculo(
        marca="Chevrolet", modelo="Tracker", anio=2021, patente="SUV444", precio=25000,
        sucursal_id=sucursal2.id, categoria="SUV", asientos=7
    )
    create_vehiculo(
        marca="Honda", modelo="CR-V", anio=2022, patente="SUV555", precio=30000,
        sucursal_id=sucursal2.id, categoria="SUV", asientos=7
    )
    create_vehiculo(
        marca="Toyota", modelo="SW4", anio=2023, patente="SUV666", precio=35000,
        sucursal_id=sucursal2.id, categoria="SUV", asientos=7
    )
    create_vehiculo(
        marca="Volkswagen", modelo="Amarok", anio=2022, patente="PKP444", precio=35000,
        sucursal_id=sucursal2.id, categoria="Pickup", asientos=5
    )
    create_vehiculo(
        marca="Ford", modelo="Ranger", anio=2021, patente="PKP555", precio=34000,
        sucursal_id=sucursal2.id, categoria="Pickup", asientos=5
    )
    create_vehiculo(
        marca="Toyota", modelo="Hilux", anio=2023, patente="PKP666", precio=36000,
        sucursal_id=sucursal2.id, categoria="Pickup", asientos=5
    )

    print("Seed ejecutado correctamente!")
