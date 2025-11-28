from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import Nota
from .forms import NotaForm
from .forms import RegistroForm


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
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Generar token 
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Crear URL de activacion
            activacion_link = request.build_absolute_uri(
                reverse("activar_cuenta", kwargs={"uidb64": uid, "token": token})
            )

            # Enviar Mail
            send_mail(
                subject="Confirmacion de cuenta - NotasApp",
                message=f"Hola {user.username}, hace click para activar tu cuenta: \n\n{activacion_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )


            messages.success(
                request,
                "Tu cuenta fue creada, Revisa tu correo electronico para confirmar el mail"
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


def activar_cuenta(request, uidb64, token):
    logout(request)
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Tu cuenta fue activada correctamente. Ya podés iniciar sesión.")
        return redirect("login")
    else:
        messages.error(request, "El enlace de activación no es válido o expiró.")
        return redirect("registro")