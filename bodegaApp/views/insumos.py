import datetime
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.template import loader
from bodegaApp.forms.adjunto import AdjuntoForm
from bodegaApp.forms.insumo import InsumoForm
from bodegaApp.models.archivos import Adjunto
from bodegaApp.models.inventario import Insumo
from bodegaApp.models.registros import Prestamo
from django.contrib.auth.decorators import login_required

section = {
    "seccionActiva": os.path.basename(__file__).replace('.py', ''),
    "title": os.path.basename(__file__).replace('.py', '').capitalize(),
}

base = "insumos/"
modals = base + "modals/"

@login_required
def verInsumos(request):
    insumos = Insumo.objects.all()
    for insumo in insumos:
        try:
            insumo.enprestamo = Prestamo.objects.filter(insumo=insumo)
        except Prestamo.DoesNotExist:
            insumo.enprestamo = None
    
    seccionActiva = section
    for insumo in insumos: 
        if insumo.descripcion and len(insumo.descripcion) > 50: 
            insumo.descripcion_corta = insumo.descripcion[:50] + "..." 
        else:
            insumo.descripcion_corta = insumo.descripcion

    context = {'insumos': insumos, 'formTitle': "Insumos", 'seccionActiva': seccionActiva}
    return render(request, 'insumos/insumos.html', context)

@login_required
def crearInsumo(request):
    if request.method == 'POST':
        for filename in request.FILES:
            imageForm = AdjuntoForm(files=request.FILES,data={
                "nombre": request.FILES[filename].name + str(datetime.datetime.now().strftime("%D%H:%M:%S")),
                "tipo": request.FILES[filename].content_type,
                "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
            })

            if imageForm.is_valid():
                adjunto = imageForm.save()
                form = InsumoForm(data={
                    "nombre": request.POST["nombre"],
                    "descripcion": request.POST["descripcion"],
                    "activo": request.POST["activo"] if "activo" in request.POST else True,
                    "adjunto": adjunto.id,
                    "categoria": request.POST["categoria"],
                    "locker": request.POST["locker"],
                    "caja": request.POST["caja"],
                })
                
                if form.is_valid():
                    form.save()
                    return render(request,'components/creadoExito.html')
                else:
                    return JsonResponse(form.errors, status=400)
    else:
        form = InsumoForm()
        imageForm = AdjuntoForm()

    return render(request, 'insumos/modals/crear.html', {"form": form, "imageForm": imageForm})


@login_required
def borrarInsumo(request, id):
    if request.method == 'POST':
        Insumo.objects.get(id=id).delete()
        return render(request, 'components/borradoExito.html')

    return render(request, 'components/seguroBorrado.html', {'id': id})

@login_required
def actualizarInsumo(request, id):
    if request.method == 'POST':
        
        if request.FILES:
            for filename in request.FILES:
                imageForm = AdjuntoForm(files=request.FILES,data={
                    "nombre": request.FILES[filename].name + str(datetime.datetime.now().strftime("%D%H:%M:%S")),
                    "tipo": request.FILES[filename].content_type,
                    "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
                })
                if imageForm.is_valid():
                    adjunto = imageForm.save()
                else:
                    return JsonResponse(imageForm.errors, status=400)
        else:
            adjunto = Adjunto.objects.get(id=Insumo.objects.get(id=id).adjunto.id)
        

        form = InsumoForm(data={
            "nombre": request.POST["nombre"],
            "descripcion": request.POST["descripcion"],
            "activo": request.POST["activo"] if "activo" in request.POST else False,
            "adjunto": adjunto.id,
            "categoria": request.POST["categoria"],
            "locker": request.POST["locker"],
            "caja": request.POST["caja"],
        }, instance=Insumo.objects.get(id=id))

        if form.is_valid():
            form.save()
            return render(request,'components/creadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)
        
        
        
    form = InsumoForm(instance=Insumo.objects.get(id=id))
    idAdjunto = Insumo.objects.get(id=id).adjunto.id
    adjunto = Adjunto.objects.get(id=idAdjunto)
    imageForm = AdjuntoForm(instance=Adjunto.objects.get(id=idAdjunto))
    return render(request, 'insumos/modals/actualizar.html', {"form": form, "imageForm": imageForm, "id": id, "adjunto": adjunto})