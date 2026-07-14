"""Tests básicos para el app `juego`.

Incluye comprobaciones sencillas sobre los archivos de imagen referenciados
por los objetos `Famoso` en el fixture de test.
"""

from django.test import TestCase
from django.core.files.storage import default_storage
from .models import Famoso


class FamosoImageTests(TestCase):
    """Verifica que al menos un `Famoso` del fixture tenga una imagen existente."""
    fixtures = ['famosos.json']

    def test_fixture_images_exist(self):
        famoso = Famoso.objects.exclude(imagen='').first()
        self.assertIsNotNone(famoso)
        self.assertTrue(default_storage.exists(famoso.imagen.name))
