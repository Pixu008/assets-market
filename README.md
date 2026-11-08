# VRC Assets Market
**Modelo de Negocio:** Marketplace de recursos digitales y assets para avatares 3D.
**Integrantes:** Andrés Maximiliano Martínez Espinoza
**Entidad de Contexto:** CategoriaAsset (ej. Texturas, PhysBones)
**Entidad Principal:** Recurso3D (Asset descargable)
**Propósito de la Sesión:** Carrito de compras digital. Los usuarios acumularán assets en su bolsa virtual para visualizar el total acumulado antes de la descarga.

## Bitácora de Uso de Inteligencia Artificial

Durante el desarrollo de **VRC Assets**, se utilizó IA como herramienta de apoyo técnico. A continuación se documentan tres casos de uso con su respectiva adaptación crítica:

### Caso 1: Arquitectura y ORM (Búsqueda Avanzada)
* **Prompt Utilizado:** "¿Cómo puedo implementar un buscador en Django que filtre un catálogo buscando coincidencias simultáneas en el título, el código y la descripción de un producto sin hacer múltiples consultas pesadas?"
* **Respuesta Técnica de la IA:** Sugirió el uso de objetos `Q` del módulo `django.db.models` para encapsular múltiples condiciones y realizar consultas tipo `OR` (`|`) a nivel de base de datos.
* **Adaptación Aplicada:** Se importó e implementó la clase `Q` en la vista `catalogo` (`views.py`). En lugar de usar la respuesta genérica, se adaptó específicamente al modelo `Recurso3D` para cruzar los campos `titulo`, `codigo_slug` y `descripcion`, optimizando el rendimiento de la búsqueda en el frontend.

### Caso 2: Manejo de Sesiones HTTP (Bolsa de Assets)
* **Prompt Utilizado:** "¿Cuál es la forma más segura y óptima de implementar un carrito de compras temporal en Django (request.session) sin afectar el rendimiento de la base de datos?"
* **Respuesta Técnica de la IA:** Recomendó crear una clase independiente orientada a objetos que encapsule el diccionario `request.session`, manejando internamente los métodos para agregar, calcular totales y vaciar la memoria.
* **Adaptación Aplicada:** Se creó el archivo `bolsa.py` exclusivo para la lógica del carrito. Se modificó el código sugerido para que solo almacene el ID, título y el `precio_clp` (evitando guardar objetos complejos que rompen la serialización JSON de las sesiones), cumpliendo con los estándares de seguridad para transacciones de assets.

### Caso 3: Operaciones CRUD y Formularios (Seguridad Multimedia)
* **Prompt Utilizado:** "¿Cómo configuro correctamente una vista de edición (Update) en Django para un ModelForm que incluye subida de imágenes, evitando sobreescribir datos por error?"
* **Respuesta Técnica de la IA:** Explicó la necesidad de inyectar `instance=objeto` tanto en métodos GET como POST, además de añadir explícitamente `request.FILES` y el atributo `enctype="multipart/form-data"` en el HTML.
* **Adaptación Aplicada:** Se implementó en la vista `editar_asset`, asegurando la carga segura de las previsualizaciones 3D y los archivos `.zip`. Además, se conectó con el sistema de `messages` de Django para proveer feedback al usuario, garantizando que el formulario HTML rechace envíos malformados.