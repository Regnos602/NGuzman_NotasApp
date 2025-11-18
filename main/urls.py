from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    #Inicio
    path("", views.inicio, name="inicio"),

    #Autenticacion
    path("login/", auth_views.LoginView.as_view(
        template_name="inicio.html" 
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),

    #Bloc de notas
    path("notas/", views.lista_notas, name="lista_notas"),
    path("notas/nueva/", views.crear_nota, name="crear_nota"),
    path("notas/<int:nota_id>/editar/", views.editar_nota, name="editar_nota"),
    path("notas/<int:nota_id>/eliminar/", views.eliminar_nota, name="eliminar_nota"),

    #Acerca
    path("acerca/", views.acerca, name="acerca"),
]