from django.urls import path
from . import views

urlpatterns = [
    path('iniciar/', views.iniciar_partida, name='iniciar_partida'),
    path('partida/', views.jugar_partida, name='jugar_partida'),
]