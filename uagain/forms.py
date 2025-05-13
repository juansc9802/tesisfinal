from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Productos


class CustomUserCreationForm(UserCreationForm):
    
        class Meta:
                model = User
                fields = ['username','first_name','last_name','email','password1', 'password2']

class ProductoForm(forms.ModelForm):
    
        class Meta:
                model = Productos
                fields = ['nombre', 'descripcion','precio', 'categoria', 'imagen']
        def clean_precio(self):
                precio = self.cleaned_data.get('precio')
                if precio <= 0:
                        raise forms.ValidationError("El precio debe ser mayor que cero.")
                return precio



class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
                