
from django.contrib import admin
from django.urls import path, include
from juego import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('juego/', include ('juego.urls')),
]
