"""Módulo de configuración del admin para el app `juego`.

Registra el modelo `Famoso` en el panel de administración y personaliza
la vista de lista (columnas, búsqueda y filtros).
"""

from django.contrib import admin
from .models import Famoso


@admin.register(Famoso)
class FamosoAdmin(admin.ModelAdmin):
    """Configuración del admin para `Famoso`.

    - `list_display`: columnas mostradas en la lista del admin.
    - `search_fields`: campos que se pueden buscar desde la barra superior.
    - `list_filter`: filtros laterales para acotar la lista por categoría.
    """
    list_display = ('nombre', 'profesion', 'edad', 'categoria')
    search_fields = ('nombre', 'profesion')
    list_filter = ('categoria',)
