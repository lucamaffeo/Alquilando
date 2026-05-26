# Alquilando

Sistema web de gestión de alquiler de vehículos desarrollado con **Flask**. Permite a usuarios registrarse, reservar vehículos, realizar pagos y calificar sus experiencias. Incluye paneles de administración y estadísticas por sucursal.

## Características

- 🚗 Gestión de vehículos y disponibilidad
- 📅 Sistema de reservas y alquileres
- 💰 Procesamiento de pagos
- ⭐ Sistema de calificaciones y reseñas
- 👥 Gestión de usuarios y empleados
- 📊 Estadísticas de alquileres por sucursal
- 🏢 Múltiples sucursales
- 🔐 Autenticación y permisos de rol

## Requisitos Previos

- Python 3.12.3 o superior
- Poetry (gestor de dependencias)
- PostgreSQL

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-repositorio>
cd Alquilando
```

### 2. Instalar dependencias con Poetry
```bash
poetry install
```

### 3. Activar el entorno virtual
```bash
poetry shell
```

### 4. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto con las configuraciones necesarias (base de datos, credenciales de correo, etc.)

### 5. Inicializar la base de datos
```bash
python -c "from src.core.database import init_db; init_db()"
```

## Inicio Rápido

Para iniciar la aplicación en modo desarrollo:

```bash
flask run --debug
```

La aplicación estará disponible en `http://localhost:5000`

## Estructura del Proyecto

```
Alquilando/
├── app.py                 # Punto de entrada principal
├── pyproject.toml         # Configuración de Poetry
├── src/
│   ├── core/             # Lógica central
│   │   ├── config.py     # Configuración
│   │   ├── database.py   # Conexión a BD
│   │   ├── models/       # Modelos de datos (SQLAlchemy)
│   │   └── repositories/ # Capa de acceso a datos
│   └── web/              # Aplicación web Flask
│       ├── controllers/  # Rutas y controladores
│       ├── templates/    # Plantillas HTML
│       └── helpers/      # Funciones auxiliares
├── static/               # Archivos estáticos (CSS, JS, imágenes)
└── resources/            # Recursos adicionales
```

## Credenciales de Prueba

### Usuario Regular
- **Email:** user@user.com
- **Contraseña:** 123456

### Empleado
- **Email:** empleado@empleado.com
- **Contraseña:** empleado123

## Dependencias Principales

- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para base de datos
- **psycopg2** - Adaptador PostgreSQL
- **Flask-Mail** - Envío de correos
- **python-dotenv** - Gestión de variables de entorno

## Desarrollo

Para ejecutar pruebas:
```bash
poetry run pytest
```

## Notas

- La aplicación utiliza PostgreSQL como base de datos
- El envío de correos está configurado para Gmail
- El modo `--debug` permite recarga automática de cambios durante el desarrollo
