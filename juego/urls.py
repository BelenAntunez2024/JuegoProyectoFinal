"""Ruteo del app `juego`.

Define las URLs locales del juego y mapea cada ruta a su vista correspondiente.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ── Autenticación ──
    path('login/', views.vista_login, name='vista_login'),
    path('registro/', views.vista_registro, name='vista_registro'),
    path('logout/', views.vista_logout, name='vista_logout'),

    # ── Recuperación de Contraseña por Correo ──
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='juego/password_reset_form.html',
             email_template_name='juego/password_reset_email.html',
             subject_template_name='juego/password_reset_subject.txt',
             success_url='/juego/password-reset/enviado/'
         ), 
         name='vista_password_reset'),

    path('password-reset/enviado/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='juego/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='juego/password_reset_confirm.html',
             success_url='/juego/password-reset/completado/'
         ), 
         name='password_reset_confirm'),

    path('password-reset/completado/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='juego/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    # ── Panel de Moderación (Permisos) ──
    path('moderador/', views.panel_moderador, name='panel_moderador'),

    # ── Juego ──
    path('', views.inicio, name='inicio'),
    path('iniciar/', views.iniciar_partida, name='iniciar_partida'),
    path('iniciar-solo/', views.iniciar_partida_solo, name='iniciar_partida_solo'),
    path('partida/', views.jugar_partida, name='jugar_partida'),
]