from django.db import models

class Famoso(models.Model):
    nombre = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100) 
    edad = models.IntegerField()
    imagen_url = models.URLField(max_length=500)
    categoria = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.profesion}"