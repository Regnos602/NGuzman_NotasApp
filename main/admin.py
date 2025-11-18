from django.contrib import admin
from .models import Nota

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "actualizada_el")
    list_filter = ("usuario", "creada_el")
    search_fields = ("titulo", "contenido")    