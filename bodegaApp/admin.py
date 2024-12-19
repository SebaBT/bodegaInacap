from django.contrib import admin
from bodegaApp.models import (
Prestamo, Usuario, Persona, Adjunto, Locker, Caja, Categoria, Insumo
)
from bodegaApp.models.registros import Registro

admin.site.register(Prestamo)
admin.site.register(Usuario)
admin.site.register(Persona)
admin.site.register(Adjunto)
admin.site.register(Locker)
admin.site.register(Caja)
admin.site.register(Categoria)
admin.site.register(Insumo)
admin.site.register(Registro)