from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    # Rutas del CRUD
    path('', views.catalogo, name='catalogo'),
    path('crear/', views.crear_asset, name='crear_asset'),
    path('editar/<slug:slug>/', views.editar_asset, name='editar_asset'),
    
    # Rutas de la Bolsa (Carrito)
    path('bolsa/agregar/<int:asset_id>/', views.agregar_a_bolsa, name='agregar_a_bolsa'),
    path('bolsa/', views.ver_bolsa, name='ver_bolsa'),
    path('bolsa/vaciar/', views.vaciar_bolsa, name='vaciar_bolsa'),
]