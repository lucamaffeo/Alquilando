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

    # Crear roles
    admin_role = create_role(name="admin", permissions=[
        user_index, user_show, user_update, user_delete,
        vehicle_create, vehicle_update, vehicle_delete, vehicle_show, vehicle_index
    ])
    usuario_role = create_role(name="usuario registrado", permissions=[
        user_show, user_update, reserva_index, reserva_show, reserva_delete,
    ])
    empleado_role = create_role(name="empleado", permissions=[
    vehicle_show, vehicle_index, vehicle_cambiar_estado, user_update, user_create_presencial,
    ])

    # Crear usuarios
    admin = create_user(
        nombre="Luca",
        email="lucamaffeo@gmail.com",
        password="admin123",  # Cambiado a 8 caracteres
        role_id=1,
        apellido="Maffeo",
        telefono="123456789",
        dni="12345678",
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
    usuario_registrado = create_user(
        nombre="usuario_registrado",
        email="user@user.com",
        password="123456",
        role_id=2,
        apellido="Di placido",
        telefono="123456789",
        dni="22222222",
        fecha_nacimiento="2000-01-01",
    )
    usuario_registrado2 = create_user(
        nombre="usuario_registrado2",
        email="user2@user.com",
        password="123456",
        role_id=2,
        apellido="Helfer",
        telefono="123456789",
        dni="33333333",
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

    # Crear modelos (si no existen)
    from src.core.models.modelo import Modelo
    def get_or_create_modelo(nombre):
        modelo = Modelo.query.filter_by(nombre=nombre).first()
        if not modelo:
            modelo = Modelo(nombre=nombre)
            db.session.add(modelo)
            db.session.commit()
        return modelo

    # Crear vehículos para ambas sucursales
    # Sucursal 1
    create_vehiculo(
        patente="ABC123", modelo_id=get_or_create_modelo("Corolla").id, marca="Toyota", categoria="Sedan", asientos=5, precio=20000, anio=2020, sucursal_id=sucursal1.id, imagen="Toyota_Corolla.png"
    )
    create_vehiculo(
        patente="DEF456", modelo_id=get_or_create_modelo("Focus").id, marca="Ford", categoria="Sedan", asientos=5, precio=18000, anio=2019, sucursal_id=sucursal1.id, imagen="Ford_Focus.png"
    )
    create_vehiculo(
        patente="SED111", modelo_id=get_or_create_modelo("Fluence").id, marca="Renault", categoria="Sedan", asientos=5, precio=21000, anio=2021, sucursal_id=sucursal1.id, imagen="Renault_Fluence.png"
    )
    create_vehiculo(
        patente="DSA242", modelo_id=get_or_create_modelo("Focus").id, marca="Ford", categoria="Sedan", asientos=5, precio=18000, anio=2019, sucursal_id=sucursal1.id, imagen="Ford_Focus.png"
    )
    create_vehiculo(
        patente="PKL205", modelo_id=get_or_create_modelo("Fluence").id, marca="Renault", categoria="Sedan", asientos=5, precio=21000, anio=2021, sucursal_id=sucursal1.id, imagen="Renault_Fluence.png"
    )

    # Sucursal 2
    create_vehiculo(
        patente="ABC456", modelo_id=get_or_create_modelo("Corolla").id, marca="Toyota", categoria="Sedan", asientos=5, precio=20000, anio=2020, sucursal_id=sucursal2.id, imagen="Toyota_Corolla.png"
    )
    create_vehiculo(
        patente="DEF789", modelo_id=get_or_create_modelo("Focus").id, marca="Ford", categoria="Sedan", asientos=5, precio=18000, anio=2019, sucursal_id=sucursal2.id, imagen="Ford_Focus.png"
    )
    create_vehiculo(
        patente="SED222", modelo_id=get_or_create_modelo("Fluence").id, marca="Renault", categoria="Sedan", asientos=5, precio=21000, anio=2021, sucursal_id=sucursal2.id, imagen="Renault_Fluence.png"
    )
    create_vehiculo(
        patente="SUV555", modelo_id=get_or_create_modelo("CR-V").id, marca="Honda", categoria="SUV", asientos=7, precio=30000, anio=2022, sucursal_id=sucursal2.id, imagen="Honda_CRV.jpg"
    )
    create_vehiculo(
        patente="SUV666", modelo_id=get_or_create_modelo("SW4").id, marca="Toyota", categoria="SUV", asientos=7, precio=35000, anio=2023, sucursal_id=sucursal2.id, imagen="Toyota_Sw4.jpg"
    )
    create_vehiculo(
        patente="PKP444", modelo_id=get_or_create_modelo("Amarok").id, marca="Volkswagen", categoria="Pickup", asientos=5, precio=35000, anio=2022, sucursal_id=sucursal2.id, imagen="Volkswagen_Amarok.png"
    )
    create_vehiculo(
        patente="PKP555", modelo_id=get_or_create_modelo("Ranger").id, marca="Ford", categoria="Pickup", asientos=5, precio=34000, anio=2021, sucursal_id=sucursal2.id, imagen="Ford_Ranger.png"
    )
    create_vehiculo(
        patente="PKP666", modelo_id=get_or_create_modelo("Hilux").id, marca="Toyota", categoria="Pickup", asientos=5, precio=36000, anio=2023, sucursal_id=sucursal2.id, imagen="Toyota_Hillux.png"
    )
   
    # Crear una reserva de ejemplo
    create_reserva(
        vehiculo_id=1,  
        user_id=usuario_registrado.id,
        fecha_inicio="2025-10-01",
        fecha_fin="2025-10-05",
    )

    print("Seed ejecutado correctamente!")
