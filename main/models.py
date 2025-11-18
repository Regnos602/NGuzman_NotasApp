from django.db import models
from django.contrib.auth.models import User

class Nota(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notas"
    )
    titulo = models.CharField(max_length=500)
    contenido = models.TextField(blank=True)
    creada_el = models.DateTimeField(auto_now_add=True)
    actualizada_el = models.DateTimeField(auto_now=True)

class Meta:
    orden = ["-actualizada_el"] #Ultimas notas arriba

def __str__(self):
    return self.titulo



