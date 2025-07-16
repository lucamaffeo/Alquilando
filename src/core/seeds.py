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
    reserva_update = create_permission(nombre="reserva_update")

    # Crear permisos de empleados
    employee_create = create_permission(nombre="employee_create")

    # Crear permisos para ver estadisticas
    estadisticas_index = create_permission(nombre="estadisticas_index")
    estadisticas_promedio = create_permission(nombre="estadisticas_promedio")
    estadisticas_alquileres = create_permission(nombre="estadisticas_alquileres")
    estadisticas_calificaciones = create_permission(nombre="estadisticas_calificaciones")

    # Crear permisos para adicionales
    adicional_index = create_permission(nombre="adicional_index")
    adicional_create = create_permission(nombre="adicional_create") 
    adicional_update = create_permission(nombre="adicional_update")
    adicional_delete = create_permission(nombre="adicional_delete")

    # Crear roles
    admin_role = create_role(name="admin", permissions=[
        user_index, user_show, user_update, user_delete,
        vehicle_create, vehicle_update, vehicle_delete, vehicle_show, vehicle_index,
        sucursal_index, sucursal_show, sucursal_create, employee_create, estadisticas_index, reserva_index, reserva_update, adicional_create, adicional_index, adicional_update, adicional_delete, estadisticas_alquileres, estadisticas_calificaciones, estadisticas_promedio
    ])
    usuario_role = create_role(name="usuario registrado", permissions=[
        user_show, user_update, reserva_index, reserva_show, reserva_delete,
    ])
    empleado_role = create_role(name="empleado", permissions=[
    vehicle_show, vehicle_index, vehicle_cambiar_estado, user_update, user_create_presencial,reserva_index,reserva_update
    ])

    # Crear usuarios
    admin3 = create_user(
        nombre="admin3",
        email="ale.proia@hotmail.com",
        password="123456",
        role_id=1,
        apellido="Proia",
        telefono="123456789",
        dni="77777777",
        fecha_nacimiento="2000-01-01",
    )
    admin4 = create_user(
        nombre="Guillermo",
        email="guillermohelfer@gmail.com",
        password="123456",
        role_id=1,
        apellido="Helfer",
        telefono="123346568",
        dni="45034325",
        fecha_nacimiento="2000-01-01",
    )
    admin = create_user(
        nombre="Luca",
        email="lucamaffeo@gmail.com",
        password="123456",
        role_id=1,
        apellido="Maffeo",
        telefono="123456789",
        dni="40882818",
        fecha_nacimiento="2000-01-01",
    )
    empleado = create_user(
        nombre="empleado",
        email="empleado@empleado.com",
        password="123456",
        role_id=3,
        apellido="Proia",
        telefono="123456789",
        dni="55555555",
        fecha_nacimiento="2000-01-01",
    )
    user = create_user(
        nombre="usuario",
        email="user@user.com",
        password="123456",
        role_id=2,
        apellido="Helfer",
        telefono="123456789",  
        dni="66666666",
        fecha_nacimiento="2000-01-01",  
    )
    usuario2 = create_user(
        nombre="usuario2",
        email="lucaaw37@gmail.com",
        password="123456",
        role_id=2,
        apellido="Maffeo",
        telefono="123456789",
        dni="88888888",
        fecha_nacimiento="2000-01-01",
    )
    usuario3 = create_user(
        nombre="usuario3",
        email="usuario3@mail.com",
        password="123456",
        role_id=2,
        apellido="Apellido3",
        telefono="11111113",
        dni="70000003",
        fecha_nacimiento="1995-01-01"
    )

    # Crear sucursales (solo 3 + 1 nueva)
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
    sucursal4 = create_sucursal(
        nombre="Sucursal Oeste",
        ubicacion="Av. Juan B. Justo 2222",
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

    # Crear 25 vehículos distribuidos en las 3 sucursales
    modelos_info = [
        ("Corolla", "Reembolso completo", "Toyota", "Sedan", 5, 20000, 2020, "Toyota_Corolla.png"),
        ("Focus", "Reembolso parcial", "Ford", "Hatchback", 5, 18000, 2018, "Ford_Focus.png"),
        ("Amarok", "Sin Reembolso", "Volkswagen", "Pickup", 5, 35000, 2022, "Volkswagen_Amarok.png"),
        ("CR-V", "Reembolso completo", "Honda", "SUV", 7, 30000, 2022, "Honda_CRV.jpg"),
        ("Hilux", "Reembolso parcial", "Toyota", "Pickup", 5, 34000, 2022, "Toyota_Hillux.png"),
        ("A3", "Sin Reembolso", "Audi", "Coupe", 2, 35000, 2022, "Audi_A3.png"),
        ("Fluence", "Reembolso completo", "Renault", "Sedan", 5, 21000, 2020, "Renault_Fluence.png"),
        ("SW4", "Reembolso completo", "Toyota", "SUV", 7, 37000, 2023, "Toyota_Sw4.jpg"),
        ("Ranger", "Reembolso parcial", "Ford", "Pickup", 5, 32000, 2021, "Ford_Ranger.png"),
    ]
    sucursales = [sucursal1, sucursal2, sucursal3]
    idx = 1
    vehiculos_demo = []
    for suc in sucursales:
        for modelo in modelos_info:
            if idx > 25:
                break
            vehiculos_demo.append(create_vehiculo(
                patente=f"ASD{idx:03d}",
                modelo_id=get_or_create_modelo(modelo[0], modelo[1]).id,
                marca=modelo[2],
                categoria=modelo[3],
                asientos=modelo[4],
                precio=modelo[5],
                anio=modelo[6],
                sucursal_id=suc.id,
                imagen=modelo[7],
                en_mantenimiento=(idx % 7 == 0),  # Algunos en mantenimiento
                inhabilitado=(idx % 8 == 0)      # Algunos inhabilitados
            ))
            idx += 1

    # Reservas para usuario2 (lucaaw37@gmail.com)
    # 3 activas
    create_reserva(
        vehiculo_id=vehiculos_demo[0].id,
        user_id=usuario2.id,
        fecha_inicio="2027-01-01",
        fecha_fin="2027-01-05",
        estado="activa",
        precio_total_vehiculo=vehiculos_demo[0].precio * 5
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[1].id,
        user_id=usuario2.id,
        fecha_inicio="2027-02-01",
        fecha_fin="2027-02-05",
        estado="activa",
        precio_total_vehiculo=vehiculos_demo[1].precio * 5
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[2].id,
        user_id=usuario2.id,
        fecha_inicio="2027-03-01",
        fecha_fin="2027-03-05",
        estado="activa",
        precio_total_vehiculo=vehiculos_demo[2].precio * 5
    )
    # 1 cancelada
    create_reserva(
        vehiculo_id=vehiculos_demo[3].id,
        user_id=usuario3.id,
        fecha_inicio="2027-04-01",
        fecha_fin="2027-04-05",
        estado="cancelada",
        precio_total_vehiculo=vehiculos_demo[3].precio * 5
    )
    # 4 finalizadas con calificación
    create_reserva(
        vehiculo_id=vehiculos_demo[4].id,
        user_id=usuario2.id,
        fecha_inicio="2024-10-01",
        fecha_fin="2024-10-05",
        estado="finalizada",
        precio_total_vehiculo=vehiculos_demo[4].precio * 5,
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[5].id,
        user_id=user.id,
        fecha_inicio="2024-09-01",
        fecha_fin="2024-09-05",
        estado="finalizada",
        precio_total_vehiculo=vehiculos_demo[5].precio * 5,
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[6].id,
        user_id=user.id,
        fecha_inicio="2024-08-01",
        fecha_fin="2024-08-05",
        estado="finalizada",
        precio_total_vehiculo=vehiculos_demo[6].precio * 5,
        calificacion=3,
        comentario="Todo ok"
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[7].id,
        user_id=usuario3.id,
        fecha_inicio="2024-07-01",
        fecha_fin="2024-07-05",
        estado="finalizada",
        precio_total_vehiculo=vehiculos_demo[7].precio * 5,
        calificacion=5,
        comentario="Perfecto"
    )

    # Reservas para otros usuarios (ejemplo)
    create_reserva(
        vehiculo_id=vehiculos_demo[8].id,
        user_id=user.id,
        fecha_inicio="2024-06-01",
        fecha_fin="2024-06-05",
        estado="finalizada",
        precio_total_vehiculo=vehiculos_demo[8].precio * 5,
        calificacion=4,
        comentario="Buen trato"
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[9].id,
        user_id=usuario3.id,
        fecha_inicio="2024-05-01",
        fecha_fin="2024-05-05",
        estado="finalizada",
        precio_total_vehiculo=vehiculos_demo[9].precio * 5,
        calificacion=2,
        comentario="Podría mejorar"
    )

    # Reservas activas adicionales (ninguna de usuario2/lucaaw37@gmail.com)
    create_reserva(
        vehiculo_id=vehiculos_demo[10].id,
        user_id=user.id,
        fecha_inicio="2027-05-01",
        fecha_fin="2027-05-05",
        estado="activa",
        precio_total_vehiculo=vehiculos_demo[10].precio * 5
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[11].id,
        user_id=usuario3.id,
        fecha_inicio="2027-06-01",
        fecha_fin="2027-06-05",
        estado="activa",
        precio_total_vehiculo=vehiculos_demo[11].precio * 5
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[12].id,
        user_id=user.id,
        fecha_inicio="2027-07-01",
        fecha_fin="2027-07-05",
        estado="activa",
        precio_total_vehiculo=vehiculos_demo[12].precio * 5
    )
    create_reserva(
        vehiculo_id=vehiculos_demo[13].id,
        user_id=usuario3.id,
        fecha_inicio="2027-08-01",
        fecha_fin="2027-08-05",
        estado="activa",
        precio_total_vehiculo=vehiculos_demo[13].precio * 5
    )

    # Crear adicionales (sin GPS)
    from src.core.models.adicional import Adicional
    adicional1 = Adicional(nombre="Silla para bebes", precio=2000)
    adicional2 = Adicional(nombre="Valija de techo", precio=3000)
    adicional3 = Adicional(nombre="Seguro completo", precio=5000)
    db.session.add_all([adicional1, adicional2, adicional3])
    db.session.commit()

    # Crear 2 vehículos nuevos iguales en la sucursal nueva
    modelo_nuevo = get_or_create_modelo("Fiesta", "Reembolso completo")
    vehiculo_oeste_1 = create_vehiculo(
        patente="OESTE001",
        modelo_id=modelo_nuevo.id,
        marca="Ford",
        categoria="Hatchback",
        asientos=5,
        precio=17000,
        anio=2021,
        sucursal_id=sucursal4.id,
        imagen="Ford_Fiesta.png",
        en_mantenimiento=True,
        inhabilitado=False
    )
    vehiculo_oeste_2 = create_vehiculo(
        patente="OESTE002",
        modelo_id=modelo_nuevo.id,
        marca="Ford",
        categoria="Hatchback",
        asientos=5,
        precio=17000,
        anio=2021,
        sucursal_id=sucursal4.id,
        imagen="Ford_Fiesta.png",
        en_mantenimiento=False,
        inhabilitado=True
    )

    # Reservas finalizadas en 2023 para esos vehículos
    create_reserva(
        vehiculo_id=vehiculo_oeste_1.id,
        user_id=user.id,
        fecha_inicio="2023-03-10",
        fecha_fin="2023-03-15",
        estado="activa",
        precio_total_vehiculo=vehiculo_oeste_1.precio * 6,
        calificacion=5,
        comentario="Muy buen Fiesta"
    )
    create_reserva(
        vehiculo_id=vehiculo_oeste_2.id,
        user_id=usuario3.id,
        fecha_inicio="2023-04-01",
        fecha_fin="2023-04-06",
        estado="finalizada",
        precio_total_vehiculo=vehiculo_oeste_2.precio * 6,
        calificacion=4,
        comentario="Cómodo y económico"
    )

    print("Seed ejecutado correctamente!")
