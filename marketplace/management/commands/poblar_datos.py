from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import CategoriaAsset, Recurso3D

class Command(BaseCommand):
    help = 'Puebla la base de datos con categorías, assets 3D y usuarios de prueba'

    def handle(self, *args, **kwargs):
        # 1. Crear Usuarios de Prueba
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@vrcmarket.cl', 'admin123')
            self.stdout.write(self.style.SUCCESS('Usuario superadmin creado.'))
            
        if not User.objects.filter(username='usuario_estandar').exists():
            User.objects.create_user('usuario_estandar', 'user@vrcmarket.cl', 'user123')
            self.stdout.write(self.style.SUCCESS('Usuario estándar creado.'))

        # 2. Crear 4 Entidades de Contexto (Categorías)
        categorias = [
            'Texturas Krita', 
            'Configuraciones PhysBones', 
            'Modelos Base', 
            'Accesorios Rindo'
        ]
        
        cat_objs = {}
        for cat_nombre in categorias:
            cat, created = CategoriaAsset.objects.get_or_create(nombre=cat_nombre)
            cat_objs[cat_nombre] = cat
            
        self.stdout.write(self.style.SUCCESS('4 categorías base creadas.'))

        # 3. Crear 8 Entidades Principales (Recursos 3D)
        assets_data = [
            {
                'categoria': cat_objs['Texturas Krita'],
                'codigo_slug': 'tex-ojos-anime',
                'titulo': 'Textura HD Ojos Anime',
                'descripcion': 'Archivo .kra con capas separadas para iris y brillos.',
                'precio_clp': 0,
                'estado': 'DISPONIBLE'
            },
            {
                'categoria': cat_objs['Texturas Krita'], 
                'codigo_slug': 'tex-ropa-cyberpunk',
                'titulo': 'Paquete Texturas Ropa Cyberpunk',
                'descripcion': 'Materiales emisivos para Unity.',
                'precio_clp': 2500,
                'estado': 'DISPONIBLE'
            },
            {
                'categoria': cat_objs['Configuraciones PhysBones'],
                'codigo_slug': 'phys-cabello-largo',
                'titulo': 'Prefab PhysBones Cabello Largo',
                'descripcion': 'Configuración optimizada de colisionadores.',
                'precio_clp': 1500,
                'estado': 'DISPONIBLE'
            },
            {
                'categoria': cat_objs['Configuraciones PhysBones'],
                'codigo_slug': 'phys-falda',
                'titulo': 'Físicas para Faldas Plisadas',
                'descripcion': 'Ajuste de Unity VCC para evitar clipping.',
                'precio_clp': 1000,
                'estado': 'EN_REVISION'
            },
            {
                'categoria': cat_objs['Modelos Base'],
                'codigo_slug': 'base-femenina',
                'titulo': 'Malla Base Femenina Low Poly',
                'descripcion': 'Modelo .fbx optimizado para VRChat.',
                'precio_clp': 5000,
                'estado': 'DISPONIBLE'
            },
            {
                'categoria': cat_objs['Modelos Base'],
                'codigo_slug': 'base-masculina',
                'titulo': 'Malla Base Masculina',
                'descripcion': 'Incluye blendshapes de expresión facial.',
                'precio_clp': 5000,
                'estado': 'DISPONIBLE'
            },
            {
                'categoria': cat_objs['Accesorios Rindo'],
                'codigo_slug': 'zapatillas-urbanas-rindo',
                'titulo': 'Zapatillas Urbanas modelo Rindo',
                'descripcion': 'Calzado ajustado a la escala del avatar Rindo.',
                'precio_clp': 3500,
                'estado': 'DISPONIBLE'
            },
            {
                'categoria': cat_objs['Accesorios Rindo'],
                'codigo_slug': 'clips-cabello-rindo',
                'titulo': 'Accesorios de Cabello Digitales',
                'descripcion': 'Clips y horquillas listas para acoplar al hueso de la cabeza.',
                'precio_clp': 800,
                'estado': 'DISPONIBLE'
            }
        ]

        for asset in assets_data:
            Recurso3D.objects.get_or_create(
                codigo_slug=asset['codigo_slug'],
                defaults=asset
            )
            
        self.stdout.write(self.style.SUCCESS('8 assets 3D creados exitosamente.'))
        self.stdout.write(self.style.SUCCESS('¡Poblado de datos finalizado!'))