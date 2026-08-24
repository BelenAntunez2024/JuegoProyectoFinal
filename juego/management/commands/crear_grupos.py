"""Comando para inicializar los grupos y roles del juego.

Ejecutar con: python manage.py crear_grupos
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from juego.models import Famoso


class Command(BaseCommand):
    help = 'Crea los grupos Jugador y Moderador con sus respectivos permisos'

    def handle(self, *args, **options):
        # 1. Crear Grupo "Jugador" (rol estándar de juego)
        grupo_jugador, created = Group.objects.get_or_create(name='Jugador')
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Grupo "Jugador" creado con éxito.'))
        else:
            self.stdout.write('ℹ️ Grupo "Jugador" ya existe.')

        # 2. Crear Grupo "Moderador" (rol con permisos de gestión de famosos)
        grupo_moderador, created = Group.objects.get_or_create(name='Moderador')
        
        # Obtener los permisos del modelo Famoso
        content_type = ContentType.objects.get_for_model(Famoso)
        permisos_famoso = Permission.objects.filter(content_type=content_type)

        # Asignar todos los permisos de Famoso al grupo Moderador
        for permiso in permisos_famoso:
            grupo_moderador.permissions.add(permiso)

        self.stdout.write(self.style.SUCCESS('✅ Grupo "Moderador" configurado con permisos de gestión de famosos.'))
