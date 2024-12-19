from django.urls import path
from bodegaApp.api.views import caja


urlpatterns = [
    path("locker/<int:id>/cajas", caja.cajas_por_locker, name="cajas_por_locker"),
]