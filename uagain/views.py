from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .models import Categoria, Productos
from .forms import ProductoForm, PerfilForm
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserChangeForm
from django.views.decorators.csrf import csrf_exempt
import json
from decimal import Decimal
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    productos = Productos.objects.all()
    pago_exitoso = request.GET.get('pago') == 'exitoso'
    return render(request, 'core/home.html', {"producto": productos, 'pago_exitoso': pago_exitoso})

@login_required
def products(request):
    producto = Productos.objects.all()
    print("Hola")
    return render(request, 'core/products.html', {"producto": producto})
@login_required
def mis_productos(request):
    producto = Productos.objects.all()
    return render(request, 'core/mis_productos.html', {"producto": producto})


def signup(request):
    return render(request, 'core/signup.html')

def exit(request):
    logout(request)
    return redirect('home')

@login_required
def aceptar_pagos(request, producto_id):

    producto = get_object_or_404(Productos, id=producto_id)
    if request.method == "POST":
            producto.aceptado = True
            producto.save()
            return redirect('products')  
    return render(request, 'core/aceptar_pagos.html', {'producto': producto})


@login_required
def perfil(request):
    return render(request, 'core/perfil.html')


def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()
        
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])

            login(request, user)
            return redirect('home')

    return render(request, 'registration/register.html',data)

def agregar_producto(request):

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creador = request.user
            producto.save()
            return redirect('products')  
    else:
        form = ProductoForm()

    return render(request, 'core/agregar_producto.html', {'form': form})

def success_view(request):
    producto_id = request.GET.get('producto_id')
    if producto_id:
        producto = get_object_or_404(Productos, id=producto_id)
        producto.aceptado = True 
        producto.save()
    return redirect('/?pago=exito')


def cancel_view(request):
    return render(request, 'core/cancel.html')




@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            producto = Productos.objects.get(id=producto_id)

            # Validar precio mínimo (por ejemplo, 1000 COP)
            if producto.precio < Decimal('1000.00'):
                return JsonResponse({'error': 'El precio mínimo para publicar es de $1000 COP'}, status=400)

            # Convertir Decimal a entero para Stripe (en centavos)
            precio_en_cop = int(producto.precio)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'cop',
                            'product_data': {
                                'name': producto.nombre,
                                'description': producto.descripcion,
                                'images': [request.build_absolute_uri(producto.imagen.url)] if producto.imagen else [],
                            },
                            'unit_amount': precio_en_cop,
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f'http://localhost:8000/success/?producto_id={producto.id}',
                cancel_url='http://localhost:8000/cancel/',
            )
            return HttpResponseRedirect(checkout_session.url)

        except Productos.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def perfil_usuario(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('perfil_usuario')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'core/perfil_usuario.html', {'form': form})   


@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id, creador=request.user)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('mis_productos')  
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'core/editar_producto.html', {'form': form})


@login_required
def chat_usuario(request, username):
    receptor = get_object_or_404(User, username=username)
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            Mensaje.objects.create(
                emisor=request.user,
                receptor=receptor,
                contenido=contenido,
                fecha=timezone.now())
            return redirect('chat_usuario', username=receptor.username)


    return render(request, 'core/chat.html', {
        'receptor': receptor
    })


@login_required
def mensajesApi(request, receptor_id):
    mensajes = Mensaje.objects.filter(
        emisor=request.user, receptor_id=receptor_id
    ) | Mensaje.objects.filter(
        emisor_id=receptor_id, receptor=request.user
    )
    mensajes = mensajes.order_by('fecha')

    data = [{
        'emisor': m.emisor.username,
        'contenido': m.contenido,
        'fecha': m.fecha.strftime('%Y-%m-%d %H:%M:%S'),
        'es_emisor': m.emisor == request.user
    } for m in mensajes]

    return JsonResponse({'mensajes': data})


@login_required
def lista_chats(request):
    mensajes = Mensaje.objects.filter(Q(emisor=request.user) | Q(receptor=request.user))
    
    usuarios = set()
    for m in mensajes:
        if m.emisor != request.user:
            usuarios.add(m.emisor)
        if m.receptor != request.user:
            usuarios.add(m.receptor)
    
    return render(request, 'core/lista_chats.html', {'usuarios': usuarios})