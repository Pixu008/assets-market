from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('crear/', views.crear_asset, name='crear_asset'),
]