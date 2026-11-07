from django.contrib import admin
from .models import CategoriaAsset, Recurso3D

# 1. Identidad Corporativa del Panel
admin.site.site_header = 'VRC Assets - Panel de Control'
admin.site.site_title = 'VRC Assets Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'

# 2. Configuración Avanzada de ModelAdmin
@admin.register(CategoriaAsset)
class CategoriaAssetAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Recurso3D)
class Recurso3DAdmin(admin.ModelAdmin):
    # Vista tabular con identificador, título, contexto, valor cuantitativo, estado y vigencia
    list_display = ('codigo_slug', 'titulo', 'categoria', 'precio_clp', 'estado', 'vigente')
    
    # Filtros laterales
    list_filter = ('categoria', 'estado', 'vigente')
    
    # Búsqueda textual
    search_fields = ('codigo_slug', 'titulo', 'descripcion')
    
    # Edición rápida directa en la grilla (campo numérico y estado)
    list_editable = ('precio_clp', 'estado')
    
    # Estructura modular del formulario en secciones lógicas temáticas (fieldsets)
    fieldsets = (
        ('Identificación del Recurso', {
            'fields': ('codigo_slug', 'titulo', 'categoria')
        }),
        ('Detalles y Atributos Comerciales', {
            'fields': ('descripcion', 'precio_clp', 'estado')
        }),
        ('Soporte Multimedia', {
            'fields': ('imagen_preview', 'archivo_zip')
        }),
        ('Control de Sistema', {
            'fields': ('vigente',)
        }),
    )