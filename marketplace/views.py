from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Recurso3D, CategoriaAsset
from .forms import Recurso3DForm

def catalogo(request):
    # Obtener solo los assets vigentes
    assets = Recurso3D.objects.filter(vigente=True)
    categorias = CategoriaAsset.objects.all()

    # Búsqueda multi-campo
    query = request.GET.get('q')
    if query:
        assets = assets.filter(
            Q(titulo__icontains=query) |
            Q(codigo_slug__icontains=query) |
            Q(descripcion__icontains=query)
        )

    # Filtro por categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        assets = assets.filter(categoria_id=categoria_id)

    # Ordenamiento
    orden = request.GET.get('orden')
    if orden == 'menor_precio':
        assets = assets.order_by('precio_clp')
    elif orden == 'mayor_precio':
        assets = assets.order_by('-precio_clp')
    else:
        assets = assets.order_by('id')

    # Paginación
    paginator = Paginator(assets, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'query': query,
        'categoria_seleccionada': categoria_id,
        'orden_seleccionado': orden
    }
    return render(request, 'marketplace/catalogo.html', context)


def crear_asset(request):
    if request.method == 'POST':
        # request.FILES es vital para recibir imágenes y zips
        form = Recurso3DForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, '¡Asset 3D creado exitosamente!')
            return redirect('marketplace:catalogo')
        else:
            messages.error(request, 'Hubo un error al crear el asset. Revisa los campos.')
    else:
        form = Recurso3DForm()

    context = {
        'form': form,
        'titulo_pagina': 'Publicar Nuevo Asset'
    }
    return render(request, 'marketplace/formulario_asset.html', context)