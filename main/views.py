from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def inicio(request):
    """Si el usuario ya esta logueado lo mando directo a la lista de notas.
    si no, muestro la pantalla de inicio con opciones para login/registro

    Args:
        request (HttpRequest): Objeto de solicitud HTTP

    Returns:
        HttpResponse | HttpResponseRedirect:
        -Retorna una direccion a la vista 'lista_notas' si el usuario esta logueado
        -Retorna la plantilla 'inicio.html' si el usuario no esta logueado. 
    """
    if request.user.is_authenticated:
        return redirect("lista_notas")
    
    form = AuthenticationForm()

    return render(request, "inicio.html", {"form": form})

def registro(request):
    """Formulario de registro del usuario

    Args:
        request (HttpRequest): Objeto de solicitud HTTP

    Returns:
        HttpResponse | HttpResponseRedirect:
        -Retorna la plantilla 'registro.html' con el formulario para registrarse.
        -Retorna una redireccion hacia 'lista_notas' si el registro se completa correctamente
        o si el usuario ya estaba registrado
    """
    if request.user.is_authenticated:
        return redirect("lista_notas")

    if request.method == "POST": 
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"¡Bienvenido/a, {user.username}! Tu cuenta se creó correctamente."
            )
            return redirect("lista_notas")
        else:
            messages.error(
                request,
                "Revisá los datos del formulario. Hay algunos errores que corregir."
            )
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})

def acerca(request):
    """Pagina de "Acerca" sobre la pagina web.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP

    Returns:
        HttpResponse: Retorna la plantilla 'acerca.html' con toda la informacion del autor
    """
    return render(request, "acerca.html")

@login_required
def lista_notas(request):
    return render(request, 'lista_notas.html')