def create_default_categoria():
    from bodegaApp.models import Categoria
    if not Categoria.objects.filter(nombreCategoria="sin categoría").exists():
        Categoria.objects.create(nombreCategoria="sin categoría")

def get_default_categoria():
    from bodegaApp.models import Categoria
    categoria, created = Categoria.objects.get_or_create(nombreCategoria="sin categoría")
    return categoria

