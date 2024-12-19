import os
from django.shortcuts import render
from bodegaApp.models.registros import Registro
from django.contrib.auth.decorators import login_required
section = {
    "seccionActiva": os.path.basename(__file__).replace('.py', ''),
    "title": os.path.basename(__file__).replace('.py', '').capitalize(),
}

base = "registros/"
modals = base + "modals/"

@login_required
def verTodosRegistros(request):
    context = {
        'registros': Registro.objects.all()
    }
        
    return render(request, base+'registros.html', {**context, **section})

@login_required
def detalleRegistro(request,id):
    context = {
        'registro': Registro.objects.get(id=id)
    }
        
    return render(request, modals+'detalles.html', {**context, **section})