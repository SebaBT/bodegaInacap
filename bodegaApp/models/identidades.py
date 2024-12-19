from django.db import models
from bodegaApp.models import Adjunto
from django.contrib.auth.models import AbstractUser
from bodegaApp.models.helpers.adjuntoDefaults import create_default_adjunto

class Persona(models.Model):
    rut                 = models.CharField(max_length=12, unique=True)
    nombre_completo     = models.CharField(max_length=75)
    fecha_nacimiento    = models.DateField()
    
    def __str__(self):
        return self.nombre_completo

class Usuario(AbstractUser):
    first_name = None
    last_name = None
    is_staff = None
    groups = None
    user_permissions = None
    
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    persona = models.OneToOneField(Persona, on_delete=models.PROTECT, unique=True)
    foto_perfil = models.ForeignKey(Adjunto, on_delete=models.SET_DEFAULT, default=1)

    
    def __str__(self):
        return self.username
