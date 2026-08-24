# 🎴 Celebrity Age Clash

> Juego web de estrategia y estimación de edades de celebridades, desarrollado con **Django**, **PostgreSQL** y **Docker**.

---

## 📋 Descripción

**Celebrity Age Clash** es un juego donde los jugadores reciben cartas de famosos y deben estimar sus edades para acercarse lo más posible a la suma de edades de la banca, sin pasarse.

### ¿Cómo se juega?

1. **La Banca** selecciona aleatoriamente 5 famosos y suma sus edades en secreto.
2. **El Jugador** pide cartas (famosos) una a una. Solo ve el nombre, la foto y la profesión — **la edad permanece oculta** durante toda la partida.
3. El jugador debe decidir cuándo **plantarse**, confiando en su conocimiento cultural para estimar las edades.
4. Al finalizar, se revelan todas las edades reales y se determina el ganador.

### Modos de juego

| Modo | Descripción |
|------|-------------|
| 🎯 **Solitario** | Un jugador contra la banca. El objetivo es acercarse lo más posible sin pasarse. |
| 👥 **Multijugador local** | Dos jugadores por turnos en el mismo dispositivo. Gana quien se acerque más a la banca. |

---

## 🛠️ Stack Tecnológico

| Tecnología | Versión | Uso |
|------------|---------|-----|
| [Python](https://www.python.org/) | 3.12 | Lenguaje principal |
| [Django](https://www.djangoproject.com/) | 5.0.4 | Framework web (backend + templates) |
| [PostgreSQL](https://www.postgresql.org/) | 16 | Base de datos relacional |
| [Docker](https://www.docker.com/) | — | Contenedorización |
| [Gunicorn](https://gunicorn.org/) | 21.2.0 | Servidor WSGI para producción |
| [Pillow](https://python-pillow.org/) | 10.3.0 | Procesamiento de imágenes |

---

## 📁 Estructura del Proyecto

```
ProyectoJuego/
├── config/                  # Configuración del proyecto Django
│   ├── settings.py          # Settings (DB, media, apps instaladas)
│   ├── urls.py              # Rutas raíz (admin + juego + media)
│   ├── wsgi.py              # Punto de entrada WSGI
│   └── asgi.py              # Punto de entrada ASGI
│
├── juego/                   # App principal del juego
│   ├── models.py            # Modelo Famoso (nombre, profesión, edad, imagen)
│   ├── views.py             # Lógica del juego (inicio, partida, turnos)
│   ├── urls.py              # Rutas del juego
│   ├── admin.py             # Configuración del panel de admin
│   ├── tests.py             # Tests unitarios
│   ├── fixtures/
│   │   └── famosos.json     # Datos precargados de +100 famosos
│   ├── templates/juego/
│   │   ├── inicio.html      # Pantalla de bienvenida / menú
│   │   ├── partida.html     # Tablero principal del juego
│   │   └── jugar.html       # Vista auxiliar
│   └── static/css/
│       ├── base.css          # Estilos globales
│       ├── inicio.css        # Estilos del menú
│       ├── partida.css       # Estilos del tablero
│       └── jugar.css         # Estilos auxiliares
│
├── media/                   # Fotos de celebridades (103 imágenes)
├── scripts/
│   └── fix_fixture_media.py # Script de mantenimiento de fixtures
│
├── Dockerfile               # Imagen Docker (Python 3.12-slim)
├── docker-compose.yml       # Orquestación: Django + PostgreSQL
├── requirements.txt         # Dependencias de Python
├── manage.py                # CLI de Django
├── .env                     # Variables de entorno (no versionado)
└── documentacion            # Documento de diseño del proyecto
```

---

## 🚀 Instalación y Puesta en Marcha

### Prerrequisitos

- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) instalados.

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd ProyectoJuego
```

### 2. Configurar variables de entorno

Crear un archivo `.env` 

### 3. Levantar los contenedores

```bash
docker-compose up --build
```

Esto levanta dos servicios:
- **db** — PostgreSQL 16 con persistencia de datos.
- **web** — Django en `http://localhost:8000`.

### 4. Ejecutar migraciones

En otra terminal (o con `docker-compose exec`):

```bash
docker-compose exec web python manage.py migrate
```

### 5. Cargar los datos de famosos

```bash
docker-compose exec web python manage.py loaddata famosos.json
```

Esto carga los **103 famosos** precargados con sus nombres, profesiones, edades y fotos.

### 6. (Opcional) Crear superusuario para el admin

```bash
docker-compose exec web python manage.py createsuperuser
```

### 7. ¡Jugar!

Abrí tu navegador en:

- 🎮 **Juego:** [http://localhost:8000/juego/](http://localhost:8000/juego/)
- ⚙️ **Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🎮 Rutas de la Aplicación

| Ruta | Descripción |
|------|-------------|
| `/juego/` | Pantalla de inicio / menú principal |
| `/juego/iniciar/` | Inicia partida multijugador (2 jugadores) |
| `/juego/iniciar-solo/` | Inicia partida solitario (1 jugador vs banca) |
| `/juego/partida/` | Tablero de la partida en curso |
| `/admin/` | Panel de administración de Django |

---

## 🧠 Arquitectura y Lógica del Juego

### Modelo de Datos

```
Famoso
├── nombre     (CharField)     → Nombre artístico o real
├── profesion  (CharField)     → Actor, Cantante, Futbolista, etc.
├── edad       (IntegerField)  → Edad real (oculta durante el juego)
├── imagen     (ImageField)    → Foto del famoso
└── categoria  (CharField)     → Cine, Música, Deportes, etc.
```

### Flujo del Juego

```
Inicio → Selección de modo → Generar banca (5 famosos aleatorios)
                                     ↓
                              Turno del jugador
                              ├── Pedir carta → Se muestra foto + nombre (sin edad)
                              └── Plantarse   → Fin del turno
                                     ↓
                              Revelación final → Se muestran todas las edades
                                     ↓
                              Resultado (quién se acercó más a la banca)
```

### Seguridad

- Las edades **nunca se envían al navegador** durante la partida.
- Toda la lógica de sumas y comparación se ejecuta **exclusivamente en el servidor** (sesiones de Django).
- Esto impide que un jugador vea las edades inspeccionando el código fuente o la consola del navegador.

---

## 🧪 Tests

Ejecutar los tests unitarios:

```bash
docker-compose exec web python manage.py test juego
```

---

## 📦 Dependencias

```
django==5.0.4
psycopg2-binary==2.9.9
django-environ==0.11.2
gunicorn==21.2.0
Pillow==10.3.0
```

---

## 👤 Autora

**Belén Antúnez** — Proyecto Final de Diplomatura (2024)

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos.
