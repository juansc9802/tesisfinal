
from django.urls import path
from uagain import views
from uagain.views import home,mis_productos,mensajesApi, editar_producto, products,signup, exit, register,agregar_producto, aceptar_pagos, perfil, create_checkout_session, success_view, cancel_view, perfil_usuario, chat_usuario

urlpatterns = [
    
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('mis_productos/', mis_productos, name='mis_productos'),
    path('signup/', signup, name='signup'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('agregar_producto/', agregar_producto, name='agregar_producto'),
    path('producto/aceptar/<int:producto_id>/', aceptar_pagos, name='aceptar_pagos'),
    path('perfil/', perfil, name='perfil'),
    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('mi-perfil/', perfil_usuario, name='perfil_usuario'),
    path('producto/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('chat/api/mensajes/<int:receptor_id>/', views.mensajesApi, name='api_mensajes'),
    path('chat/<str:username>/', chat_usuario, name='chat_usuario'),
    path('chats/', views.lista_chats, name='lista_chats'),


]