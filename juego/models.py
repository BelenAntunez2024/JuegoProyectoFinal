"""Modelos del app `juego`.

Contiene la definición de `Famoso`, la entidad principal del juego que
representa a cada carta/personaje con su nombre, profesión, edad y opcionalmente
una imagen. Los comentarios en los campos explican la intención de cada uno.
"""

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
    
    # ImageField: guarda la foto en el servidor en la carpeta MEDIA_ROOT.
    # Se mantiene en la raíz de media para que coincida con los archivos ya existentes.
    # blank=True, null=True → el campo no es obligatorio, por si hay famosos sin foto.
    imagen = models.ImageField(upload_to='', blank=True, null=True)
    
    # Campo opcional para filtrar famosos por categoría (Ej: Cine, Música, Deportes)
    categoria = models.CharField(max_length=50, blank=True)

    class Meta:
        # Permiso personalizado para diferenciar Moderadores de Jugadores comunes
        permissions = [
            ("puede_moderar", "Puede acceder al panel de moderación y gestionar famosos"),
        ]


    def __str__(self):
        # Define cómo se ve el objeto en el panel de administración de Django
        return f"{self.nombre} - {self.profesion}"