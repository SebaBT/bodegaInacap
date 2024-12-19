from django.db import models
from bodegaApp.models.archivos import Adjunto
from bodegaApp.models.inventario import Categoria, Caja, Insumo, Locker
from bodegaApp.models.identidades import Persona, Usuario
from django.core import serializers


class Prestamo(models.Model):
    ESTADO_CHOICES = (
        (1, 'En préstamo'),
        (2, 'Devuelto'),
        (3, 'Perdido'),
        (4, 'Anulado'),
        (5, 'Otros'),
    )
    
    usuario        = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    solicitante    = models.ForeignKey(Persona, on_delete=models.PROTECT)
    adjunto        = models.ForeignKey(Adjunto, on_delete=models.PROTECT, null=True, blank=True)
    insumo         = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    fechaCreacion  = models.DateTimeField(auto_now_add=True)
    ubicacion      = models.CharField(max_length=255)
    notas          = models.TextField()
    estado         = models.IntegerField(choices=ESTADO_CHOICES, default=1)


    def __str__(self):
        return f"{self.solicitante.nombre_completo} - {self.insumo.nombre}"

    def get_estado_display(self):
        return dict(Prestamo.ESTADO_CHOICES)[self.estado]
    
    def save(self,**kwargs):
        super().save( **kwargs)
        if self.estado == 1:
            return Insumo.objects.filter(id=self.insumo.id).update(activo=False)
        if self.estado == 2:
            return Insumo.objects.filter(id=self.insumo.id).update(activo=True)
        if self.estado == 3:
            return Insumo.objects.filter(id=self.insumo.id).update(activo=False)
        if self.estado == 4:
            return Insumo.objects.filter(id=self.insumo.id).update(activo=True)
        if self.estado == 5:
            return Insumo.objects.filter(id=self.insumo.id).update(activo=True)



class Registro(models.Model):
    user = models.CharField(max_length=255) 
    nombreTabla = models.CharField(max_length=255)
    modeloPrevio = models.JSONField()
    modeloNuevo = models.JSONField()
    action = models.CharField(max_length=16, null=False, blank=True)
    timestamp = models.DateTimeField(auto_now=True)