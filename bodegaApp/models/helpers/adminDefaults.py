from django.contrib.auth.hashers import make_password
def create_default_admin():
    from bodegaApp.models import Usuario,Adjunto,Persona
    Usuario.objects.create(
        email="admin@admin.com" ,
        username="admin",
        password=make_password("admin"),
        persona=Persona.objects.get(id=1),
        foto_perfil=Adjunto.objects.get(id=1),
        is_superuser=True
    )
    
def create_default_person():
    from bodegaApp.models import Persona
    Persona.objects.create(
        rut="11.111.111-1",
        nombre_completo="admin",
        fecha_nacimiento="2003-11-11"
    )