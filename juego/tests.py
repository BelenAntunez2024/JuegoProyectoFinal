from django.test import TestCase
from django.core.files.storage import default_storage
from .models import Famoso


class FamosoImageTests(TestCase):
    fixtures = ['famosos.json']

    def test_fixture_images_exist(self):
        famoso = Famoso.objects.exclude(imagen='').first()
        self.assertIsNotNone(famoso)
        self.assertTrue(default_storage.exists(famoso.imagen.name))
