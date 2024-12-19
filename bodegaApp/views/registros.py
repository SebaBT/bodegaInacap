import os
from django.shortcuts import render
from bodegaApp.models.registros import Registro

section = {
    "seccionActiva": os.path.basename(__file__).replace('.py', ''),
    "title": os.path.basename(__file__).replace('.py', '').capitalize(),
}

base = "registros/"
modals = base + "modals/"

def verTodosRegistros(request):
    context = {
        'registros': Registro.objects.all()
    }
        
    return render(request, base+'registros.html', {**context, **section})