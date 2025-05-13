from django.contrib import admin
from .models import Categoria, Productos

admin.site.register(Categoria)
admin.site.register(Productos)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion','precio', 'categoria', 'imagen')
# Register your models here.
