from django.db import models

class Adjunto(models.Model):
    adjunto = models.FileField(upload_to='adjuntos/')
    nombre = models.CharField(max_length=500)
    fecha = models.DateField(auto_now=True)
    tipo = models.CharField(max_length=30)
    
    def __str__(self):
        return self.adjunto.url