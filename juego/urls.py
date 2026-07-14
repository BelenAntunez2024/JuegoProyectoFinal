"""Ruteo del app `juego`.

Define las URLs locales del juego y mapea cada ruta a su vista correspondiente.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Página de bienvenida / menú
    path('', views.inicio, name='inicio'),

    # Rutas para iniciar una partida en modos disponibles
    path('iniciar/', views.iniciar_partida, name='iniciar_partida'),
    path('iniciar-solo/', views.iniciar_partida_solo, name='iniciar_partida_solo'),

    # Ruta del tablero de la partida
    path('partida/', views.jugar_partida, name='jugar_partida'),
]
