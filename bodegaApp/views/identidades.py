import datetime
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.template import loader
from bodegaApp.forms.adjunto import AdjuntoForm
from bodegaApp.forms.persona import PersonaForm
from bodegaApp.forms.usuario import UsuarioForm
from bodegaApp.models.archivos import Adjunto
from bodegaApp.models.identidades import Persona, Usuario
from django.contrib.auth.decorators import login_required
section = {
    "seccionActiva": os.path.basename(__file__).replace('.py', ''),
    "title": os.path.basename(__file__).replace('.py', '').capitalize(),
}

base = "identidades/"
modals = base + "modals/"

@login_required
def crearPersona(request):
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'components/creadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)
    else:
        form = PersonaForm()

    return render(request, modals+'crearPersona.html', {"form": form})

@login_required
def crearUsuario(request):
    if request.method == 'POST':
        for filename in request.FILES:
            imageForm = AdjuntoForm(files=request.FILES,data={
            "nombre": request.FILES[filename].name + str(datetime.datetime.now().strftime("%D%H:%M:%S")),
            "tipo": request.FILES[filename].content_type,
            "fecha": datetime.datetime.now().strftime("%d-%m-%Y")
            })
        
        if imageForm.is_valid():
            adjunto = imageForm.save()
            form = UsuarioForm(data={
                "username": request.POST["username"],
                "email": request.POST["email"],
                "password": request.POST["password"],
                "persona": request.POST["persona"],
                "is_superuser": request.POST["is_superuser"] if "is_superuser" in request.POST else False,
                "foto_perfil": adjunto.id
            })
            
            if form.is_valid():
                usuario = form.save(commit=False)
                usuario.password = make_password(usuario.password) 
                usuario.save()
                return render(request,'components/creadoExito.html')
            else:
                return JsonResponse(form.errors, status=400)
    else:
        form = UsuarioForm()
        imageForm = AdjuntoForm()

    return render(request, modals+'crearUsuario.html', {"form": form, "imageForm": imageForm})





def borrarUsuario(request, id):
    if request.method == 'POST':
        Usuario.objects.get(id=id).delete()
        return render(request, 'components/borradoExito.html')

    return render(request, 'components/seguroBorrado.html', {'id': id})

def borrarPersona(request, id):
    if request.method == 'POST':
        Persona.objects.get(id=id).delete()
        return render(request, 'components/borradoExito.html')

    return render(request, 'components/seguroBorrado.html', {'id': id})

def detalleUsuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, base+'detalleUsuario.html', {'usuario': usuario})

def actualizarPersona(request, id):
    if request.method == 'POST':
        form = PersonaForm(request.POST, instance=Persona.objects.get(id=id))
        if form.is_valid():
            form.save()
            return render(request,'components/actualizadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)
    else:
        form = PersonaForm(instance=Persona.objects.get(id=id))

    return render(request, modals+'actualizarPersona.html', {"form": form, "id": id})


def actualizarUsuario(request, id):
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
            adjunto = Adjunto.objects.get(id=Usuario.objects.get(id=id).foto_perfil.id)
        
        form = UsuarioForm(data={
                "username": request.POST["username"],
                "email": request.POST["email"],
                "password": request.POST["password"],
                "persona": request.POST["persona"],
                "is_superuser": request.POST["is_superuser"] if "is_superuser" in request.POST else False,
                "foto_perfil": adjunto.id
            }, instance=Usuario.objects.get(id=id))
            
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = make_password(usuario.password) 
            usuario.save()
            return render(request,'components/actualizadoExito.html')
        else:
            return JsonResponse(form.errors, status=400)
            
    form = UsuarioForm(instance=Usuario.objects.get(id=id))
    idAdjunto = Usuario.objects.get(id=id).foto_perfil.id
    adjunto = Adjunto.objects.get(id=idAdjunto)
    imageForm = AdjuntoForm(instance=adjunto)

    return render(request, modals+'actualizarUsuario.html', {"form": form, "imageForm": imageForm, "id": id, "adjunto": adjunto})

def verUsuarios(request):
    context = {
        'usuarios': Usuario.objects.all()
    }
    return render(request, base+'verUsuarios.html', {**context, **section})

def verPersonas(request):
    personas = Persona.objects.all()
    for persona in personas:
        try:
            persona.usuario = Usuario.objects.get(persona=persona)
        except Usuario.DoesNotExist:
            persona.usuario = None

    context = {
        'personas': personas
    }
    return render(request, base+'verPersonas.html', {**context, **section})

