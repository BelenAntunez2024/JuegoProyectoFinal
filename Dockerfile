# 1. Usamos una imagen base oficial de Python muy ligera (slim)
FROM python:3.12-slim

# 2. Configuración de Python:
# - PYTHONDONTWRITEBYTECODE=1: Evita que Python escriba archivos .pyc en el disco del contenedor
# - PYTHONUNBUFFERED=1: Envía los prints y logs directamente a la terminal sin guardarlos en buffer, 
#   permitiendo debuguear en tiempo real.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecemos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiamos los requisitos primero (aprovecha la caché de Docker al reconstruir)
COPY requirements.txt .

# 5. Instalamos las dependencias de Django y PostgreSQL
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos todo el código de nuestra aplicación local al contenedor
COPY . .

# 7. Exponemos el servidor de desarrollo de Django en el puerto 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]