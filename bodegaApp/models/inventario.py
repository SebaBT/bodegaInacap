from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ValidationError
from bodegaApp.models.archivos import Adjunto
from bodegaApp.models.helpers.categoriaDefaults import get_default_categoria

class Locker(models.Model):
    nameTag             = models.CharField(max_length=6)
    comentario          = models.TextField()
    
    #* Claves foreaneas
    adjunto          = models.ForeignKey(Adjunto, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = "Locker"
        verbose_name_plural = "Lockers"

    def __str__(self):
        return self.nameTag

class Caja(models.Model):
    nameTag             = models.CharField(max_length=6)
    activo              = models.BooleanField()
    
    #* Claves foreaneas
    adjunto           = models.ForeignKey(Adjunto, on_delete=models.PROTECT)
    locker            = models.ForeignKey(Locker, on_delete=models.PROTECT, blank=False, null=False)
    
    
    class Meta:
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"

    def __str__(self):
        return self.nameTag









class Categoria(models.Model):
    def clean(self):
        super().clean()
        self.nombreCategoria = self.nombreCategoria.lower()
        
    def __str__(self):
        return self.nombreCategoria.capitalize()
    
    nombreCategoria = models.CharField(max_length=20, unique=True)
    
    
    
    
class Insumo(models.Model):
    nombre          = models.CharField(max_length=100)
    descripcion     = models.CharField(max_length=500)
    activo          = models.BooleanField(default=True)
    #* Claves Foraneas
    adjunto         = models.ForeignKey(Adjunto, on_delete=models.PROTECT)
    categoria       = models.ForeignKey(Categoria,on_delete=models.SET(get_default_categoria), default=get_default_categoria)
    locker          = models.ForeignKey(Locker, on_delete=models.PROTECT, null=True, blank=True)
    caja            = models.ForeignKey(Caja, on_delete=models.PROTECT, null=True, blank=True)
    
    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"

    def __str__(self):
        return self.nombre
    
    def clean(self):
        super().clean()
        if self.caja and not self.locker:
            raise ValidationError("Un insumo debe estar en un locker si está en una caja.",)