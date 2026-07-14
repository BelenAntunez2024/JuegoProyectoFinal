"""Configuración del app `juego`.

Contiene la clase `JuegoConfig` usada por Django para registrar metadatos
del paquete en `INSTALLED_APPS`.
"""

from django.apps import AppConfig


class JuegoConfig(AppConfig):
    """Define la configuración y metadatos del app `juego`."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'juego'
