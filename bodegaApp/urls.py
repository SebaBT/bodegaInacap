from django.urls import include, path
from bodegaApp.views.bodega import actualizarCaja, actualizarLocker, borrarCaja, borrarLocker, detallesCaja, detallesLocker, verBodega, verCaja, verInsumo, verLocker, moverCaja, moverInsumo, crearCaja, crearLocker
from bodegaApp.views.identidades import actualizarPersona, actualizarUsuario, borrarPersona, borrarUsuario, crearPersona, crearUsuario, detalleUsuario, verPersonas, verUsuarios
from bodegaApp.views.insumos import actualizarInsumo, borrarInsumo, crearInsumo, verInsumos
from bodegaApp.views.outside import login_view
from bodegaApp.views.prestamos import actualizarPrestamo, crearPrestamo, detallesPrestamo, verPrestamos
from bodegaApp.views.registros import verTodosRegistros
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    # Sección fuera de panel
    path("", verBodega, name="Home"),
    path('login/', login_view, name='Login'),
    
    
    # Bodega
    path("bodega/", verBodega, name="Bodega"),
    path("bodega/locker/<int:id>/", verLocker, name="BodegaLocker"),
    path("bodega/caja/<int:id>/", verCaja, name="BodegaCaja"),
    path("bodega/insumos/<int:id>/", verInsumo, name="BodegaInsumo"),
    
    ##NOTE - Mover
    path("bodega/mover/caja/<int:id>/", moverCaja, name="MoverCaja"),
    path("bodega/mover/insumo/<int:id>", moverInsumo, name="MoverInsumo"),
    
    #NOTE - Crear
    path("crear/caja/", crearCaja, name="CrearCaja"),
    path("crear/caja/<int:id>", crearCaja, name="CrearCaja"),
    path("crear/locker/", crearLocker, name="CrearLocker"),
    
    #NOTE - Borrar
    path("borrar/caja/", borrarCaja, name="BorrarCaja"),
    path("borrar/caja/<int:id>/", borrarCaja, name="BorrarCaja"),
    path("borrar/locker/", borrarLocker, name="BorrarLocker"),
    path("borrar/locker/<int:id>/", borrarLocker, name="BorrarLocker"),
    
    #NOTE - Actualizar
    path("actualizar/Caja/", actualizarCaja, name="ActualizarCaja"),
    path("actualizar/Locker/", actualizarLocker, name="ActualizarLocker"),
    path("actualizar/Caja/<int:id>/", actualizarCaja, name="ActualizarCaja"),
    path("actualizar/Locker/<int:id>/", actualizarLocker, name="ActualizarLocker"),
    
    #NOTE - Detalles
    path("detalles/caja/<int:id>/", detallesCaja, name="DetallesCaja"),
    path("detalles/locker/<int:id>/", detallesLocker, name="DetallesLocker"),
    
    
    
    
    
    
    
    # Prestamos
    path("prestamos/", verPrestamos, name="Prestamos"),
    path("crearPrestamos/", crearPrestamo, name="CrearPrestamo"),
    path("actualizarPrestamos/<int:id>", actualizarPrestamo, name="ActualizarPrestamo"),
    path("detallesPrestamos/<int:id>", detallesPrestamo, name="DetallesPrestamo"),
    
    # Registros
    path("registros/", verTodosRegistros, name="Registros"),
    
    # Insumos
    path("insumos/", verInsumos, name="Insumos"),
    path("crearInsumo/", crearInsumo, name="CrearInsumo"),
    
    path("borrarInsumo/", borrarInsumo, name="BorrarInsumo"),
    path("borrarInsumo/<int:id>/", borrarInsumo, name="BorrarInsumo"),
    
    path("actualizarInsumo/<int:id>/", actualizarInsumo, name="ActualizarInsumo"),
    path("detallesInsumo/<int:id>/", verInsumo, name="DetallesInsumo"),
    
    
    
    # Identidades
    path("usuarios/", verUsuarios, name="Usuarios"),
    path("personas/", verPersonas, name="Personas"),
    
    path("verUsuario/<int:id>/", detalleUsuario, name="DetallesUsuario"),
    
    
    path("actualizarUsuario/", actualizarUsuario, name="ActualizarUsuario"),
    path("actualizarPersona/", actualizarPersona, name="ActualizarPersona"),
    path("actualizarUsuario/<int:id>/", actualizarUsuario, name="ActualizarUsuario"),
    path("actualizarPersona/<int:id>/", actualizarPersona, name="ActualizarPersona"),

    path('crearUsuario/', crearUsuario, name='CrearUsuario'),
    path('crearPersona/', crearPersona, name='CrearPersona'),
    
    path("borrarUsuario/", borrarUsuario, name="BorrarUsuario"),
    path("borrarPersona/", borrarPersona, name="BorrarPersona"),
    
    path("borrarUsuario/<int:id>/", borrarUsuario, name="BorrarUsuario"),
    path("borrarPersona/<int:id>/", borrarPersona, name="BorrarPersona"),
    
    
    #SECTION - API
    path("api/", include('bodegaApp.api.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)