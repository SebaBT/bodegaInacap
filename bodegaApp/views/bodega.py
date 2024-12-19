import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from bodegaApp.forms.caja import CajaMover
from bodegaApp.forms.insumo import InsumoMover
from bodegaApp.models import Caja, Insumo, Locker
from bodegaApp.forms.adjunto import AdjuntoForm
from bodegaApp.forms.caja import CajaForm
from bodegaApp.forms.locker import LockerForm
import datetime
from django.contrib.auth.decorators import login_required
from bodegaApp.models.archivos import Adjunto
from bodegaApp.models.identidades import Usuario

section = {
    "seccionActiva": os.path.basename(__file__).replace('.py', ''),
    "title": os.path.basename(__file__).replace('.py', '').capitalize(),
    }

base = "bodega/"
modals = base + "modals/"

@login_required
def verBodega(request):
    
    lockers = Locker.objects.all()
    for locker in lockers:
        try:
            locker.habitado = Caja.objects.filter(locker=locker) or Insumo.objects.filter(locker=locker)
        except Caja.DoesNotExist or Insumo.DoesNotExist:
            locker.habitado = None

    context = {
        'lockers': lockers, 
    }
    
    return render(request, base+'bodega.html', { **context, **section })


@login_required
def verLocker(request, id):

    cajas = Caja.objects.filter(locker=id)
    for caja in cajas:
        try:
            caja.habitado = Insumo.objects.filter(caja=caja)
        except Caja.DoesNotExist or Insumo.DoesNotExist:
            caja.habitado = None

    context = {
        "cajas": cajas,
        "insumos": Insumo.objects.filter(locker=id, caja__isnull=True),
        "locker": Locker.objects.get(id=id),
    }
    
    
    
    return render(request, modals+'contenidoLocker.html', { **context, **section })

@login_required
def verCaja(request, id):
    
    context = {
        "caja": Caja.objects.get(id=id),
        "insumos": Insumo.objects.filter(caja=id),
    }
    
    return render(request, modals+'contenidoCaja.html', { **context})

@login_required
def verInsumo(request, id):
    
    context = {
        "insumo": Insumo.objects.get(id=id),
    }
    
    return render(request, 'insumos/modals/detalles.html', { **context })

@login_required
def moverCaja(request, id):
    caja = Caja.objects.get(id=id)
    
    if request.method == 'POST':
        form = CajaMover(request.POST, instance=caja)
        if form.is_valid():
            caja = form.save()
            locker = Locker.objects.get(id=caja.locker.id)
            
            Insumo.objects.filter(caja=caja).update(locker=locker.id)
            
            return render(request, 'components/moverExito.html')

    form = CajaMover(instance=caja)
    context = {'form': form, 'locker_viejo': caja.locker , "caja": caja}
    
    return render(request, modals+'moverCaja.html', { **context, **section })

@login_required
def moverInsumo(request, id):
    insumo = Insumo.objects.get(id=id)
    if request.method == 'POST':
        form = InsumoMover(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            return render(request, 'components/moverExito.html')
    else:
        form = InsumoMover(instance=insumo)

    context = {'form': form, 'locker_viejo': insumo.locker, 'caja_vieja': insumo.caja}
    return render(request, modals+'moverInsumoModal.html', { **context, **section })

@login_required
def borrarCaja(request, id):
    caja = Caja.objects.get(id=id)
    caja.delete()
    return redirect('base')

@login_required
def crearCaja(request,id=None):
    if request.method == 'POST':
        for filename in request.FILES:
            imageForm = AdjuntoForm(files=request.FILES,data={
                "nombre": request.FILES[filename].name + str(datetime.datetime.now().strftime("%D%H:%M:%S")),
                "tipo": request.FILES[filename].content_type,
                "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
            })
        
            if imageForm.is_valid():
                adjunto = imageForm.save()
                form = CajaForm(data={
                    "nameTag": request.POST["nameTag"],
                    "activo": True,
                    "adjunto": adjunto.id,
                    "locker": request.POST["locker"],
                })
                
                if form.is_valid():
                    form.save()
                    return render(request,'components/creadoExito.html')
            
    else:
        form = CajaForm()
        imageForm = AdjuntoForm()
        if id:
            form = CajaForm(data= {
                "locker": id
            })

    return render(request, modals+'crearCaja.html', {"form": form, "imageForm": imageForm})

@login_required
def crearLocker(request):
    if request.method == 'POST':
        for filename in request.FILES:
            imageForm = AdjuntoForm(files=request.FILES,data={
                "nombre": request.FILES[filename].name + str(datetime.datetime.now().strftime("%D%H:%M:%S")),
                "tipo": request.FILES[filename].content_type,
                "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
            })
            
            if imageForm.is_valid():
                adjunto = imageForm.save()
                form = LockerForm(data={
                    "nameTag": request.POST["nameTag"],
                    "comentario": request.POST["comentario"],
                    "adjunto": adjunto.id,
                })
            else:
                return JsonResponse(imageForm.errors, status=400)
                
            if form.is_valid():
                locker = form.save(commit=False)
                locker.save()
                return render(request,'components/creadoExito.html')
            else:
                return JsonResponse(form.errors, status=400)
    else:
        form = LockerForm()
        imageForm = AdjuntoForm()

    return render(request, modals+'crearLocker.html', {"form": form, "imageForm": imageForm})


@login_required
def borrarCaja(request, id):
    if request.method == 'POST':
        Caja.objects.get(id=id).delete()
        return render(request, 'components/borradoExito.html')

    return render(request, 'components/seguroBorrado.html', {'id': id})

@login_required
def borrarLocker(request, id):
    if request.method == 'POST':
        Locker.objects.get(id=id).delete()
        return render(request, 'components/borradoExito.html')

    return render(request, 'components/seguroBorrado.html', {'id': id})



@login_required
def actualizarCaja(request, id):
    if request.method == 'POST':
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
            adjunto = Adjunto.objects.get(id=Caja.objects.get(id=id).adjunto.id)

        form = CajaForm(data={
            "nameTag": request.POST["nameTag"],
            "activo": request.POST["activo"] if "activo" in request.POST else False,
            "adjunto": adjunto.id,
            "locker": Caja.objects.get(id=id).locker.id,
        }, instance=Caja.objects.get(id=id))

        if form.is_valid():
            form.save()
            return render(request, 'components/actualizadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)

    else:
        form = CajaForm(instance=Caja.objects.get(id=id))
        idAdjunto = Caja.objects.get(id=id).adjunto.id
        adjunto = Adjunto.objects.get(id=idAdjunto)
        imageForm = AdjuntoForm(instance=adjunto)

    return render(request, modals+'actualizarCaja.html', {"form": form, "imageForm": imageForm, "id": id, "adjunto": adjunto})


@login_required
def actualizarLocker(request, id):
    if request.method == 'POST':
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
            adjunto = Adjunto.objects.get(id=Locker.objects.get(id=id).adjunto.id)
            
        form = LockerForm(data={
            "nameTag": request.POST["nameTag"],
            "comentario": request.POST["comentario"],
            "adjunto": adjunto.id,
        }, instance=Locker.objects.get(id=id))

        if form.is_valid():
            form.save()
            return render(request, 'components/actualizadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)
    else:
        form = LockerForm(instance=Locker.objects.get(id=id))
        idAdjunto = Locker.objects.get(id=id).adjunto.id
        adjunto = Adjunto.objects.get(id=idAdjunto)
        imageForm = AdjuntoForm(instance=adjunto)


    return render(request, modals+'actualizarLocker.html', {"form": form, "imageForm": imageForm, "id": id, "adjunto": adjunto})

@login_required
def detallesCaja(request, id):
    
    context = {
        "caja": Caja.objects.get(id=id),
    }
    
    return render(request, modals+'detallesCaja.html', { **context })

@login_required
def detallesLocker(request, id):
    
    context = {
        "locker": Locker.objects.get(id=id),
    }
    
    return render(request, modals+'detallesLocker.html', { **context })