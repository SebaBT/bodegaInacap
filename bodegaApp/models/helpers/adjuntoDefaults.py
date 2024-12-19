def create_default_adjunto():
    from django.core.files.base import ContentFile
    from bodegaApp.models import Adjunto
    if not Adjunto.objects.filter(nombre="defaultProfilePicture").exists():
        try:
            with open("uploads/defaultProfilePicture.png", "rb") as f:
                content = f.read()
                Adjunto.objects.get_or_create(
                    adjunto=ContentFile(content, name='defaultProfilePicture.png'),
                    nombre="defaultProfilePicture",
                    tipo="png"
                )
        except FileNotFoundError:
            print("Default profile picture not found. Ensure 'uploads/defaultProfilePicture.png' exists.")
