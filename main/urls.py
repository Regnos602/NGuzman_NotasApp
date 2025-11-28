from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Inicio
    path("", views.inicio, name="inicio"),

    # Autenticacion
    path("login/", auth_views.LoginView.as_view(
        template_name="inicio.html" 
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),

    # Bloc de notas
    path("notas/", views.lista_notas, name="lista_notas"),
    path("notas/nueva/", views.crear_nota, name="crear_nota"),
    path("notas/<int:nota_id>/editar/", views.editar_nota, name="editar_nota"),
    path("notas/<int:nota_id>/eliminar/", views.eliminar_nota, name="eliminar_nota"),

    # Acerca
    path("acerca/", views.acerca, name="acerca"),

    # Activacion de cuenta
    path("activar/<uidb64>/<token>/", views.activar_cuenta, name="activar_cuenta"),

    # Recuperar contraseña
    path("password-reset/", 
        auth_views.PasswordResetView.as_view(), 
        name="password_reset"),

    path("password-reset/enviado/", 
        auth_views.PasswordResetDoneView.as_view(), 
        name="password_reset_done"),

    path("password-reset/confirm/<uidb64>/<token>/", 
        auth_views.PasswordResetConfirmView.as_view(), 
        name="password_reset_confirm"),

    path("password-reset/completo/", 
        auth_views.PasswordResetCompleteView.as_view(), 
        name="password_reset_complete"),
]