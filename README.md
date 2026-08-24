# 🎴 Celebrity Age Clash — Trabajo Final

> **Producto Mínimo Viable (PMV)**: Juego web interactivo de estrategia, intuición y estimación de edades de celebridades.  
> Desarrollado con **Django 5**, **PostgreSQL 16** y **Docker**.

---

## 🚀 Puesta en Marcha (1 Solo Comando)

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd ProyectoJuego
```

### 2. Levantar la aplicación
```bash
docker compose up --build
```
> ⚡ **Automatización Total**: Este único comando levanta PostgreSQL y Django, aplica las migraciones de base de datos, carga las cartas de famosos (`famosos.json`), configura los roles de usuario (`Jugador` y `Moderador`) y crea el usuario administrador por defecto automáticamente.

### 3. Abrir en el navegador
👉 **[http://localhost:8000/juego/](http://localhost:8000/juego/)**

---

## 🔑 Credenciales por Defecto

| Rol | Usuario | Contraseña | Permisos |
|---|---|---|---|
| 🛡️ **Administrador / Moderador** | `admin` | `adminpassword123` | Jugar + Panel de Moderación + Gestión de Famosos y Usuarios en Django Admin |
| 👤 **Jugador Estándar** | *(Crear en "Registrate acá")* | *(La que elijas)* | Jugar partidas en Modo Solitario o Multijugador |

---

## 🎮 ¿Cómo probar las funcionalidades del trabajo?

### 1. Sistema de Autenticación (Login / Registro / Logout)
- Ingresá a `http://localhost:8000/juego/login/`
- Registrá un nuevo jugador en **"Registrate acá"**.
- Al ingresar, verás la bienvenida con tu nombre de usuario y el botón para cerrar sesión.
- Si intentás entrar directamente a `http://localhost:8000/juego/partida/` sin iniciar sesión, serás redirigido al login.

### 2. Recuperación de Contraseña por Correo
- En la pantalla de login, hacé clic en **"¿Olvidaste tu contraseña?"**.
- Ingresá tu correo registrado.
- Recibirás las instrucciones de recuperación por correo electrónico (o visible en los logs de la terminal de Docker en modo desarrollo).

### 3. Permisos y Roles de Usuario
- **Como Jugador**: Solo tenés acceso a jugar partidas en **Modo Solitario** o **Multijugador**.
- **Como Moderador / Admin** (iniciando con `admin` / `adminpassword123`): Verás la insignia dorada **`MODERADOR`** y el botón **"🛡️ Acceder al Panel de Moderador"**, donde podés ver métricas y acceder al panel de administración para gestionar la base de famosos.

### 4. Dinámica del Juego
1. La **Banca** selecciona 5 famosos al azar y suma sus edades en secreto.
2. El **Jugador** pide cartas para acercarse a la suma de la banca sin pasarse. Las edades permanecen ocultas durante la partida.
3. El jugador decide cuándo **plantarse**. Al finalizar, se revelan las edades reales y se determina el ganador.

---


## 📁 Estructura del Proyecto

```
ProyectoJuego/
├── config/                                 # Configuración principal de Django
│   ├── settings.py                         # Configuración (DB, Auth, Email, Media)
│   ├── urls.py                             # Enrutamiento raíz (/admin/, /juego/)
│   ├── wsgi.py                             # Punto de entrada WSGI
│   └── asgi.py                             # Punto de entrada ASGI
│
├── juego/                                  # Aplicación principal del juego
│   ├── admin.py                            # Configuración del panel de administración
│   ├── apps.py                             # Configuración del app
│   ├── forms.py                            # Formularios de Registro y Login
│   ├── models.py                           # Modelo Famoso (con permiso personalizado 'puede_moderar')
│   ├── tests.py                            # Tests unitarios
│   ├── urls.py                             # Rutas locales (Login, Registro, Password Reset, Juego, Moderador)
│   ├── views.py                            # Lógica del juego, autenticación y permisos
│   │
│   ├── fixtures/
│   │   └── famosos.json                    # Datos precargados de +100 celebridades
│   │
│   ├── management/
│   │   └── commands/
│   │       └── crear_grupos.py             # Comando personalizado para crear roles Jugador/Moderador
│   │
│   ├── static/css/                         # Hojas de estilo modulares (Tema Dark Neon)
│   │   ├── auth.css                        # Estilos de Login, Registro y Recuperación
│   │   ├── base.css                        # Variables globales, tipografía y botones
│   │   ├── inicio.css                      # Estilos de la pantalla de bienvenida
│   │   ├── jugar.css                       # Estilos auxiliares
│   │   └── partida.css                     # Estilos del tablero de juego
│   │
│   └── templates/juego/                    # Plantillas HTML del juego
│       ├── inicio.html                     # Menú principal y bienvenida de usuario
│       ├── login.html                      # Pantalla de inicio de sesión
│       ├── moderador.html                  # Panel exclusivo de moderación y métricas
│       ├── partida.html                    # Tablero dinámico de juego
│       ├── password_reset_complete.html    # Confirmación de clave restablecida
│       ├── password_reset_confirm.html     # Formulario para ingresar nueva contraseña
│       ├── password_reset_done.html        # Aviso de correo de recuperación enviado
│       ├── password_reset_email.html       # Cuerpo del correo con enlace dinámico
│       ├── password_reset_form.html        # Solicitud de recuperación por correo
│       ├── password_reset_subject.txt      # Asunto del correo de recuperación
│       └── registro.html                   # Formulario de registro de nuevo jugador
│
├── media/                                  # Fotografías de celebridades
├── scripts/
│   └── fix_fixture_media.py                # Script de mantenimiento de fixtures
│
├── .env.example                            # Plantilla de variables de entorno
├── Dockerfile                              # Imagen Docker optimizada (Python 3.12-slim)
├── docker-compose.yml                      # Orquestación de servicios (Django + PostgreSQL 16)
├── requirements.txt                        # Dependencias del proyecto
└── manage.py                               # CLI de Django
```

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Propósito |
|---|---|---|
| **Python** | 3.12 | Lenguaje de programación |
| **Django** | 5.0.4 | Framework backend, sistema de autenticación y templates |
| **PostgreSQL** | 16 | Base de datos relacional |
| **Docker & Compose** | — | Contenedorización y despliegue automatizado |
| **Bootstrap** | 5.3 | Sistema de grillas y componentes base |
| **CSS3** | — | Diseño responsivo modular Dark Neon / Glassmorphism |

---

## 🧠 Arquitectura y Seguridad del Juego

### Modelo de Datos
```
Famoso
├── nombre     (CharField)     → Nombre artístico o real
├── profesion  (CharField)     → Actor, Cantante, Futbolista, etc.
├── edad       (IntegerField)  → Edad real (oculta durante la partida)
├── imagen     (ImageField)    → Foto del famoso
└── categoria  (CharField)     → Cine, Música, Deportes, etc.
```

### Seguridad y Lógica en el Servidor
- **Anti-Cheat:** Las edades de las cartas **nunca se envían al navegador** mientras la partida está en curso. Toda la comparación y suma se gestiona en la sesión del servidor (Django sessions).
- **Protección CSRF:** Todas las solicitudes POST de formularios (login, registro, reseteo de clave y acciones de juego) están protegidas contra ataques de falsificación de peticiones.
- **Control de Acceso:** Vistas protegidas con decoradores `@login_required` y `@permission_required('juego.puede_moderar')`.

---
### Video de la APLICACION

https://www.youtube.com/watch?v=JvfDhB-r3iA

---

## 👤 Autora

**Belén Antúnez** — Proyecto Final de Diplomatura (2024)

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos bajo licencia libre.

