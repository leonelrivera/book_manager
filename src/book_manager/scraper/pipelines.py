import difflib
import re
import unicodedata
from datetime import datetime
from typing import Any, List, Optional
from scrapy.exceptions import DropItem

from book_manager.scraper.items import LibroCompetidorItem


def normalizar_texto(texto: Optional[str]) -> str:
    """Normaliza texto eliminando diacríticos, mayúsculas y caracteres especiales."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto))
    sin_tildes = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s]", " ", sin_tildes.lower()).strip()


class ValidacionLibroPipeline:
    """Pipeline para verificar completitud y correspondencia de título y autor con el catálogo."""

    STOP_WORDS = {
        "de", "la", "el", "los", "las", "un", "una", "en", "para", "y", "a", "del", "al", "con", "por"
    }

    def process_item(self, item: LibroCompetidorItem, spider: Optional[Any] = None) -> LibroCompetidorItem:
        """Valida que los campos obligatorios existan y correspondan al libro del catálogo propio.

        Args:
            item: Instancia de LibroCompetidorItem extraída por la spider.
            spider: Instancia opcional del Spider en ejecución.

        Returns:
            LibroCompetidorItem validado y complementado.

        Raises:
            DropItem: Si el precio es inválido o el ítem no coincide con el libro de nuestro catálogo.
        """
        titulo_comp = item.get("titulo_competidor") or ""
        titulo_int = item.get("titulo_interno") or ""
        autor_comp = item.get("autor_competidor") or ""
        autor_int = item.get("autor_interno") or ""

        if not titulo_comp:
            raise DropItem("Ítem descartado: Título de competidor no especificado.")

        precio = item.get("precio")
        if precio is None or precio <= 0:
            if not item.get("precio_texto"):
                raise DropItem(f"Ítem descartado ('{titulo_comp}'): Precio inválido o ausente.")

        # 1. Validación de correspondencia de TÍTULO
        if titulo_int:
            t_int_norm = normalizar_texto(titulo_int)
            t_comp_norm = normalizar_texto(titulo_comp)

            # Extraer palabras significativas del título interno
            palabras_int = [
                p for p in t_int_norm.split()
                if p not in self.STOP_WORDS and (len(p) > 2 or p.isdigit())
            ]
            if palabras_int:
                coincidencias = sum(
                    1 for p in palabras_int
                    if re.search(rf"\b{re.escape(p)}\b", t_comp_norm)
                )
                umbral_palabras = max(1, len(palabras_int) // 2)
                if coincidencias < umbral_palabras:
                    raise DropItem(
                        f"Ítem descartado: '{titulo_comp}' no coincide con el título buscado '{titulo_int}'."
                    )

        # 2. Validación de correspondencia de AUTOR
        if autor_int:
            a_int_norm = normalizar_texto(autor_int)
            tokens_autor = [p for p in a_int_norm.split() if len(p) > 3]

            if tokens_autor:
                if autor_comp:
                    a_comp_norm = normalizar_texto(autor_comp)
                    coincide_autor = any(
                        bool(re.search(rf"\b{re.escape(tok)}\b", a_comp_norm))
                        for tok in tokens_autor
                    )
                    if not coincide_autor:
                        raise DropItem(
                            f"Ítem descartado: '{titulo_comp}' del autor '{autor_comp}' no coincide con el autor esperado '{autor_int}'."
                        )
                else:
                    # Si Cúspide no expuso autor_competidor de forma explícita,
                    # comprobar si el autor figura en la descripción o si el título tiene alta similitud
                    desc_norm = normalizar_texto(item.get("descripcion", ""))
                    coincide_en_desc = any(
                        bool(re.search(rf"\b{re.escape(tok)}\b", desc_norm))
                        for tok in tokens_autor
                    )
                    t_int_norm = normalizar_texto(titulo_int)
                    t_comp_norm = normalizar_texto(titulo_comp)
                    ratio_titulo = difflib.SequenceMatcher(None, t_int_norm, t_comp_norm).ratio()
                    if not coincide_en_desc and ratio_titulo < 0.55:
                        raise DropItem(
                            f"Ítem descartado: '{titulo_comp}' no tiene autor válido y difiere del título buscado '{titulo_int}'."
                        )

        # Asegurar fecha de extracción si no fue fijada por el loader
        if not item.get("fecha_extraccion"):
            item["fecha_extraccion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Completar valores por defecto para campos opcionales
        if not item.get("descripcion"):
            item["descripcion"] = f"Sinopsis oficial de {titulo_comp} en Cúspide Libros."

        if not item.get("formas_pago"):
            item["formas_pago"] = "Tarjetas de crédito, débito y transferencias bancarias"

        if not item.get("url_imagen"):
            item["url_imagen"] = "Sin imagen disponible"

        return item


class AlmacenamientoItemsPipeline:
    """Pipeline para recolectar los ítems validados en una lista interna de la spider."""

    def open_spider(self, spider: Optional[Any] = None) -> None:
        """Inicializa la lista de resultados recolectados al comenzar el rastreo."""
        if spider is not None and not hasattr(spider, "items_scraped"):
            spider.items_scraped = []

    def process_item(self, item: LibroCompetidorItem, spider: Optional[Any] = None) -> LibroCompetidorItem:
        """Agrega una copia en formato diccionario del ítem a la lista de la spider."""
        if spider is not None and hasattr(spider, "items_scraped"):
            spider.items_scraped.append(dict(item))
        return item
