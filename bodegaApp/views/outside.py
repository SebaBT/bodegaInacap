import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.template import loader
from bodegaApp.forms import usuario
from bodegaApp.forms.persona import PersonaForm
from bodegaApp.forms.usuario import UsuarioForm
from bodegaApp.models.identidades import Usuario

global section
section = os.path.basename(__file__).replace('.py', '')

def login_view(request):
    if request.method == 'POST':
        form = usuario.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('Bodega')
            else:
                form.add_error(None, "Contraseña o usuario invalidos.")
    else:
        form = usuario.LoginForm()
    return render(request, 'login.html', {'form': form})