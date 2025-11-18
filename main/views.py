from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Nota
from .forms import NotaForm


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
        request (HttpRequest):Solicitud HTTP

    Returns:
        HttpResponse: Retorna la plantilla 'acerca.html' con toda la informacion del autor
    """
    return render(request, "acerca.html")

@login_required
def lista_notas(request):
    """Muestra la lista de notas de un usuario logueado

    Args:
        request (HttpRequest):Solicitud HTTP

    Returns:
        HttpResponse: Html renderizado de 'notas/lista.html' con todas las notas del usuario 
    """
    notas = Nota.objects.filter(usuario=request.user)
    return render(request, 'notas/lista.html', {"notas": notas}) 

@login_required
def crear_nota(request):
    """Funcion de creacion de nota con todas sus validaciones respectivas

    Args:
        request (HttpRequest):Solicitud HTTP

    Returns:
        HttpResponse: Si la nota se guardo te redirecciona a la lista de notas, sino al formulario
    """
    if request.method == "POST":
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user
            nota.save()
            messages.success(request, "Nota creada correctamente.")
            return redirect("lista_notas")
    else:
        form = NotaForm()
    
    return render(request, "notas/form.html", {"form": form, "modo":"crear"})


@login_required
def editar_nota(request, nota_id):
    """Funcion utilizada para editar una nota, buscandola y tirando error si no existe o es una nota
    de otro usuario, de lo contrario permite hacer las modificaciones que el usuario desee

    Args:
        request (HttpRequest): Solicitud HTTP.
        nota_id (Int): Id de la nota a editar.

    Returns:
        HttpResponse: Si la nota fue actualizada redirecciona a la lista, sino 
        muestra el form con los datos previos.
    """

    nota = get_object_or_404(Nota, id=nota_id, usuario=request.user)

    if request.method == "POST":
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, "Nota actualizada correctamente.")
            return redirect("lista_notas")
    else:
        form = NotaForm(instance=nota)

    return render(request, "notas/form.html", {"form": form, "modo": "editar"})

@login_required
def eliminar_nota(request, nota_id):
    """Funcion que permite al usuario eliminar una nota siempre y cuando exista y sea suya.

    Args:   
        request (HttpRequest): Solicitud HTTP.
        nota_id (Int): Id de la nota a editar.

    Returns:
        HttpResponse: Redirecciona a la lista de notas
    """

    nota = get_object_or_404(Nota, id=nota_id, usuario=request.user)

    if request.method == "POST":
        nota.delete()
        messages.success(request, "Nota eliminada.")
        return redirect("lista_notas")

    return render(request, "notas/confirmar_eliminar.html", {"nota": nota})

