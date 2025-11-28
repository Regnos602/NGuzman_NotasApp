from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Nota

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electronico")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo electrónico.")
        return email


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ["titulo", "contenido"]
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Titulo de la nota"
            }),
            "contenido": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Escribi aca tus ideas"
            }),
        }

        labels = {
            "titulo" : "Titulo",
            "contenido" : "Contenido",
        }