import datetime
import os
from django.http import JsonResponse
from django.shortcuts import render
from bodegaApp.forms.adjunto import AdjuntoForm
from bodegaApp.forms.prestamo import PrestamoForm
from bodegaApp.models import Prestamo
from bodegaApp.models.archivos import Adjunto
from bodegaApp.models.identidades import Usuario
from bodegaApp.models.inventario import Insumo
from django.contrib.auth.decorators import login_required

section = {
    "seccionActiva": os.path.basename(__file__).replace('.py', ''),
    "title": os.path.basename(__file__).replace('.py', '').capitalize(),
}

base = "prestamos/"
modals = base + "modals/"

@login_required
def verPrestamos(request):
    context = {'prestamos': Prestamo.objects.all()}
    return render(request, base+"prestamos.html", { **context, **section })

@login_required
def crearPrestamo(request):
    form = PrestamoForm()
    imageForm = AdjuntoForm()
    
    if request.method == 'POST':
        form  = PrestamoForm(request.POST)
        if request.FILES:
            for filename in request.FILES:
                imageForm = AdjuntoForm(files=request.FILES, data={
                    "nombre": request.FILES[filename].name + str(datetime.datetime.now().strftime("%D%H:%M:%S")),
                    "tipo": request.FILES[filename].content_type,
                    "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
                })
        
        if imageForm.is_valid():
            adjunto = imageForm.save()
        else:
            return JsonResponse(imageForm.errors, status=400)
            
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.adjunto = adjunto
            prestamo.usuario = request.user if request.user.is_authenticated else Usuario.objects.get(id=1)
            Insumo.objects.filter(id=prestamo.insumo.id).update(activo=False)
            prestamo.save()
            return render(request, 'components/creadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)
    
    context = {'form': form, 'imageForm': imageForm}
    return render(request, modals+"crear.html", { **context,**section })

@login_required
def actualizarPrestamo(request, id=None):
    prestamo = Prestamo.objects.get(id=id)
    form = PrestamoForm(instance=prestamo, initial={'insumo': prestamo.insumo})
    imageForm = AdjuntoForm(instance=prestamo.adjunto)
    
    if request.method == 'POST':
        form  = PrestamoForm(request.POST, instance=Prestamo.objects.get(id=id))
        if request.FILES:
            for filename in request.FILES:
                imageForm = AdjuntoForm(files=request.FILES, data={
                    "nombre": request.FILES[filename].name + str(datetime.datetime.now().strftime("%D%H:%M:%S")),
                    "tipo": request.FILES[filename].content_type,
                    "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
                })
                if imageForm.is_valid():
                    adjunto = imageForm.save()
                else:
                    return JsonResponse(imageForm.errors, status=400)
        else:
            adjunto = Adjunto.objects.get(id=prestamo.adjunto.id)
        
        if form.is_valid():
            
            if prestamo.insumo.id != form.cleaned_data['insumo'].id:
                Insumo.objects.filter(id=prestamo.insumo.id).update(activo=True)
            
            prestamo = form.save(commit=False)
            prestamo.adjunto = adjunto
            prestamo.usuario = request.user if request.user.is_authenticated else Usuario.objects.get(id=1)
            Insumo.objects.filter(id=prestamo.insumo.id).update(activo=False)
            prestamo.save()
            return render(request, 'components/creadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)
    
    context = {'form': form, 'imageForm': imageForm,"prestamo": prestamo}
    return render(request, modals+"actualizar.html", { **context,**section })

@login_required
def detallesPrestamo(request,id):
    context = {
        "prestamo": Prestamo.objects.get(id=id),
    }
    return render(request, modals+"detalles.html", { **context,**section })