# CanchaTulcán

Sistema web de gestión de reservas de canchas deportivas públicas del GAD de Tulcán.

## Stack tecnológico

- **Backend:** Python 3.13, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-WTF, Flask-Bcrypt
- **Base de datos:** PostgreSQL 17
- **Frontend:** HTML5, Bootstrap 5, Jinja2, JavaScript Vanilla
- **Arquitectura:** Application Factory + Blueprints modulares

## Estructura del proyecto

```
canchatulcan/
├── app/
│   ├── auth/            # Login, registro
│   ├── dashboard/        # Panel principal por rol
│   ├── usuarios/         # CRUD usuarios y roles (RF-013)
│   ├── canchas/          # CRUD canchas
│   ├── reservas/         # Calendario, reservas, historial
│   ├── pagos/            # Órdenes de pago, comprobantes, validación
│   ├── ocupaciones/       # Ocupaciones especiales (institucional/campeonato/mantenimiento)
│   ├── reportes/          # Reportes exportables CSV
│   ├── notifications/     # Notificaciones internas
│   ├── models/            # Modelos SQLAlchemy
│   ├── static/            # CSS, JS, uploads, imágenes
│   ├── templates/         # base.html, layout.html, navbar.html, sidebar.html
│   └── utils/             # permissions, decorators, helpers
├── migrations/
├── run.py
└── requirements.txt
```

## Roles del sistema

| Rol | Permisos principales |
|---|---|
| **Administrador GAD** | Acceso total: usuarios, canchas, validación de pagos, reportes |
| **Dirigente Barrial** | Gestión de canchas/ocupaciones, consulta de reservas, reportes |
| **Deportista** | Consultar disponibilidad, reservar, cancelar, subir comprobante |

## Requisitos previos

- Python 3.13
- PostgreSQL 17 en ejecución
- pip / venv

## Instalación local

```bash
# 1. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env          # Windows
cp .env.example .env            # Linux/Mac
# Editar .env con tus credenciales de PostgreSQL

# 4. Crear la base de datos
createdb canchatulcan

# 5. Aplicar migraciones
flask db upgrade

# 6. Cargar datos de demostración
flask seed-db

# 7. Ejecutar el servidor de desarrollo
python run.py
```

La aplicación quedará disponible en `http://localhost:5000`.

## Comandos útiles

```bash
# Generar una nueva migración tras modificar modelos
flask db migrate -m "descripcion del cambio"

# Aplicar migraciones pendientes
flask db upgrade

# Revertir la última migración
flask db downgrade

# Cargar datos de demostración (usuarios, canchas, horarios, reservas)
flask seed-db
```

## Usuarios de demostración

| Rol | Email | Contraseña |
|---|---|---|
| Administrador | admin@canchatulcan.com | Admin123* |
| Dirigente Barrial | dirigente@canchatulcan.com | Admin123* |
| Deportista | deportista@canchatulcan.com | Admin123* |

## Ejecución con Docker

```bash
docker-compose up --build
```

Esto levanta PostgreSQL 17 y la aplicación web. Luego, dentro del contenedor `web`:

```bash
docker-compose exec web flask db upgrade
docker-compose exec web flask seed-db
```

## Estados y colores del calendario (RF-002 / RF-012)

| Color | Estado |
|---|---|
| 🟢 Verde | Libre |
| 🔴 Rojo | Ocupado |
| 🟡 Amarillo | Pendiente de pago |
| 🟠 Naranja | Validando comprobante |
| 🔵 Azul | Ocupación institucional |
| 🟣 Morado | Campeonato |
| ⚪ Gris | Mantenimiento |
