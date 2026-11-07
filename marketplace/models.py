from django.db import models
from django.core.validators import MinValueValidator

class CategoriaAsset(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Categoría")
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Recurso3D(models.Model):
    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible para Descarga'),
        ('SUSPENDIDO', 'Suspendido Temporalmente'),
        ('EN_REVISION', 'En Revisión por Staff'),
    ]

    categoria = models.ForeignKey(CategoriaAsset, on_delete=models.PROTECT, verbose_name="Categoría del Asset")
    codigo_slug = models.SlugField(max_length=50, unique=True, verbose_name="Código/Slug")
    titulo = models.CharField(max_length=150, verbose_name="Título del Recurso")
    descripcion = models.TextField(verbose_name="Descripción Técnica")
    
    precio_clp = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Precio (CLP)")
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    imagen_preview = models.ImageField(upload_to='assets_previews/', verbose_name="Imagen de Previsualización")
    archivo_zip = models.FileField(upload_to='assets_files/', blank=True, null=True, verbose_name="Archivo del Asset")
    vigente = models.BooleanField(default=True, verbose_name="Vigente en el sistema")

    def __str__(self):
        return self.titulo