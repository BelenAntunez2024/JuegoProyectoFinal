from django.db import models

class Famoso(models.Model):
    """
    MODELO FAMOSO:
    Define la estructura de la tabla 'juego_famoso' en PostgreSQL.
    Cada registro representa a un famoso del cual los jugadores estimarán su edad.
    """
    # Nombre artístico o real del famoso
    nombre = models.CharField(max_length=100)
    
    # Su profesión (Ej: Actor, Cantante, Futbolista) para dar pistas al usuario
    profesion = models.CharField(max_length=100) 
    
    # La edad real (Dato crítico que se oculta durante la partida)
    edad = models.IntegerField()
    
    # Enlace a la imagen online del famoso
    imagen_url = models.URLField(max_length=500)
    
    # Campo opcional para filtrar famosos por categoría (Ej: Cine, Música, Deportes)
    categoria = models.CharField(max_length=50, blank=True)

    def __str__(self):
        # Define cómo se ve el objeto en el panel de administración de Django
        return f"{self.nombre} - {self.profesion}"