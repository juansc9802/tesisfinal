from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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
        fields = ['first_name', 'last_name', 'email']
                
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Contraseña actual", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Confirmar nueva contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))