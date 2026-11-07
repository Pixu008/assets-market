from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Recurso3D, CategoriaAsset
from .forms import Recurso3DForm
from .bolsa import Bolsa 

def catalogo(request):
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

def editar_asset(request, slug):
    asset = get_object_or_404(Recurso3D, codigo_slug=slug)
    
    if request.method == 'POST':
        form = Recurso3DForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, f'¡Asset "{asset.titulo}" actualizado correctamente!')
            return redirect('marketplace:catalogo')
        else:
            messages.error(request, 'Error al actualizar. Revisa los datos ingresados.')
    else:
        form = Recurso3DForm(instance=asset)

    context = {
        'form': form,
        'titulo_pagina': 'Editar Asset'
    }
    return render(request, 'marketplace/formulario_asset.html', context)

# ==========================================
# VISTAS DEL CARRITO DE COMPRAS (BOLSA)
# ==========================================

def agregar_a_bolsa(request, asset_id):
    bolsa = Bolsa(request)
    asset = get_object_or_404(Recurso3D, id=asset_id)
    bolsa.agregar(asset)
    messages.success(request, f'"{asset.titulo}" fue agregado a tu bolsa.')
    return redirect('marketplace:catalogo')

def ver_bolsa(request):
    bolsa = Bolsa(request)
    # Convertimos el diccionario a una lista para el HTML
    items_bolsa = list(bolsa.bolsa.values())
    
    context = {
        'items': items_bolsa,
        'total': bolsa.total_pagar(),
        'cantidad': bolsa.cantidad_total()
    }
    return render(request, 'marketplace/bolsa.html', context)

def vaciar_bolsa(request):
    bolsa = Bolsa(request)
    bolsa.vaciar()
    messages.info(request, 'Tu bolsa ha sido vaciada.')
    return redirect('marketplace:ver_bolsa')