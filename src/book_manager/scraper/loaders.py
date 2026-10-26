"""Módulo de cargadores de ítems (ItemLoaders) e input/output processors.

Permite transformar, limpiar y normalizar los datos crudos extraídos de las páginas
web antes de ser asignados al ítem estructurado.
"""

import re
from typing import Any, Optional
from itemloaders import ItemLoader
from itemloaders.processors import Join, MapCompose, TakeFirst

from book_manager.scraper.items import LibroCompetidorItem


def limpiar_texto(valor: Optional[str]) -> Optional[str]:
    """Limpia espacios en blanco redundantes y saltos de línea de una cadena."""
    if not valor:
        return None
    texto = re.sub(r"\s+", " ", str(valor)).strip()
    return texto if texto else None


def normalizar_precio(valor: Optional[str]) -> Optional[float]:
    """Extrae y normaliza el valor numérico decimal de un precio en texto.

    Maneja formatos como '$ 34.500,00' o '34500.00' convirtiéndolo a float.
    """
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        return float(valor)

    texto = str(valor).strip()
    # Remover símbolo de moneda y caracteres no numéricos excepto coma y punto
    texto_limpio = re.sub(r"[^\d.,]", "", texto)
    if not texto_limpio:
        return None

    # Si contiene punto como separador de miles y coma como decimal
    if "." in texto_limpio and "," in texto_limpio:
        texto_limpio = texto_limpio.replace(".", "").replace(",", ".")
    elif "," in texto_limpio:
        texto_limpio = texto_limpio.replace(",", ".")
    # Si contiene solo puntos y más de uno, es separador de miles
    elif texto_limpio.count(".") > 1:
        partes = texto_limpio.split(".")
        texto_limpio = "".join(partes[:-1]) + "." + partes[-1]

    try:
        return float(texto_limpio)
    except ValueError:
        return None


class LibroCompetidorLoader(ItemLoader):
    """Cargador especializado para poblar y limpiar instancias de LibroCompetidorItem."""

    default_item_class = LibroCompetidorItem
    default_output_processor = TakeFirst()

    titulo_interno_in = MapCompose(limpiar_texto)
    autor_interno_in = MapCompose(limpiar_texto)
    titulo_competidor_in = MapCompose(limpiar_texto)
    autor_competidor_in = MapCompose(limpiar_texto)
    precio_in = MapCompose(normalizar_precio)
    precio_texto_in = MapCompose(limpiar_texto)
    url_imagen_in = MapCompose(limpiar_texto)
    url_libro_in = MapCompose(limpiar_texto)
    fecha_extraccion_in = MapCompose(limpiar_texto)

    descripcion_in = MapCompose(limpiar_texto)
    descripcion_out = Join(" ")

    formas_pago_in = MapCompose(limpiar_texto)
    formas_pago_out = Join(" | ")
