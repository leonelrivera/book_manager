"""Definición de modelos de datos (Items) para el scraper de libros competidores.

Define la estructura de los elementos extraídos de sitios de librerías online
como Cúspide para su posterior procesamiento, validación y comparación.
"""

from typing import Any
import scrapy


class LibroCompetidorItem(scrapy.Item):
    """Item que representa los datos extraídos de un libro de la competencia."""

    titulo_interno = scrapy.Field()      # Título del libro correspondiente en el catálogo propio
    autor_interno = scrapy.Field()       # Autor correspondiente en el catálogo propio
    titulo_competidor = scrapy.Field()   # Título publicado en el sitio del competidor
    autor_competidor = scrapy.Field()    # Autor extraído de la publicación del competidor
    precio = scrapy.Field()              # Precio actual (float o numérico normalizado)
    precio_texto = scrapy.Field()        # Precio en texto tal como aparece en la web
    url_imagen = scrapy.Field()          # URL absoluta de la portada del libro
    formas_pago = scrapy.Field()         # Opciones de financiación y formas de pago
    descripcion = scrapy.Field()         # Sinopsis o descripción detallada del libro
    url_libro = scrapy.Field()           # Enlace a la ficha individual del libro
    fecha_extraccion = scrapy.Field()    # Fecha y hora en formato ISO de la extracción
