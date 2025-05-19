from src.core.database import db
from src.core.repositories.rol import create_role
from src.core.repositories.user import create_user
from src.core.repositories.permission import create_permission 
from src.core.repositories.vehiculo import create_vehiculo

def run():
    # Crear permisos de usuarios
    user_index = create_permission(nombre="user_index")
    user_show = create_permission(nombre="user_show")
    user_create = create_permission(nombre="user_create")
    user_update = create_permission(nombre="user_update")
    user_delete = create_permission(nombre="user_delete")

    # Crear permisos de vehículos
    vehicle_index = create_permission(nombre="vehicle_index")
    vehicle_show = create_permission(nombre="vehicle_show")
    vehicle_create = create_permission(nombre="vehicle_create")
    vehicle_update = create_permission(nombre="vehicle_update")
    vehicle_delete = create_permission(nombre="vehicle_delete")

    # Crear roles
    admin_role = create_role(name="admin", permissions=[
        user_index, user_show, user_create, user_update, user_delete,
        vehicle_create, vehicle_update, vehicle_delete, vehicle_show, vehicle_index
    ])
    usuario_role = create_role(name="usuario registrado", permissions=[
        user_index, user_show, user_create, user_update
    ])
    empleado_role = create_role(name="empleado", permissions=[
        vehicle_update, user_create, vehicle_show, vehicle_index
    ])

    # Crear usuarios
    admin = create_user(
        nombre="admin",
        email="admin@admin.com",
        password="admin",
        role_id=1,
        apellido="Maffeo",
        telefono="123456789",
        dni="12345678",
        fecha_nacimiento="2000-01-01",
    )
    empleado = create_user(
        nombre="empleado",
        email="empleado@empleado.com",
        password="empleado",
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


    #crear vehiculo

    vehiculo1 = create_vehiculo(
        marca="Toyota",
        modelo="Corolla",
        anio=2020,
        color="Rojo",
        patente="ABC123",
        precio=20000,
        usuario_id=1,
    )

    print("Seed ejecutado correctamente!")
