"""Ruteo del app `juego`.

Define las URLs locales del juego y mapea cada ruta a su vista correspondiente.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ── Autenticación ──
    # Pantalla de login (primera página que ve el usuario)
    path('login/', views.vista_login, name='vista_login'),
    # Pantalla de registro de nuevo usuario
    path('registro/', views.vista_registro, name='vista_registro'),
    # Cierre de sesión (no tiene pantalla, solo redirige)
    path('logout/', views.vista_logout, name='vista_logout'),

    # ── Juego ──
    # Página de bienvenida / menú (requiere login)
    path('', views.inicio, name='inicio'),
    # Rutas para iniciar una partida en modos disponibles
    path('iniciar/', views.iniciar_partida, name='iniciar_partida'),
    path('iniciar-solo/', views.iniciar_partida_solo, name='iniciar_partida_solo'),
    # Ruta del tablero de la partida
    path('partida/', views.jugar_partida, name='jugar_partida'),
]
