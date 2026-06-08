from django.contrib import admin
from .models import Famoso

@admin.register(Famoso)
class FamosoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesion', 'edad', 'categoria') # Columnas que verás en la lista
    search_fields = ('nombre', 'profesion') # Barra de búsqueda
    list_filter = ('categoria',) # Filtros laterales
