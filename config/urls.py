from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ==============================================================================
# RUTAS PRINCIPALES DE LA APLICACIÓN
# ==============================================================================
urlpatterns = [
    # Panel de administración de Django (acceso para cargar famosos, gestionar datos)
    path('admin/', admin.site.urls),
    # Incluye todas las rutas definidas en juego/urls.py bajo el prefijo /juego/
    path('juego/', include('juego.urls')),
]

# ==============================================================================
# SERVICIO DE ARCHIVOS DE MEDIA EN DESARROLLO
# ==============================================================================
# En modo DEBUG, le indicamos a Django que también sirva las imágenes subidas
# desde la carpeta MEDIA_ROOT. En producción, esto lo haría un servidor como Nginx.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
