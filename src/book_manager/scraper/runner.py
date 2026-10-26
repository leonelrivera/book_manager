"""Módulo orquestador y ejecutor de spiders para Scrapy.

Permite invocar CuspideSpider de forma programática y aislada mediante subprocesos
o CrawlerProcess, evitando el error ReactorNotRestartable de Twisted en ejecuciones
reiteradas desde la interfaz de consola interactiva o notebooks de Google Colab.
"""

import json
import os
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional


def ejecutar_scraper(
    libros: Optional[List[str]] = None,
    max_resultados: int = 10,
    archivo_salida: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Ejecuta CuspideSpider y retorna los ítems extraídos como una lista de diccionarios.

    Args:
        libros: Lista de títulos de libros de nuestro catálogo a buscar. Si es None,
            la spider consulta automáticamente el inventario actual.
        max_resultados: Límite de resultados por búsqueda (por defecto 10).
        archivo_salida: Ruta opcional donde guardar el archivo JSON con los resultados.

    Returns:
        List[Dict[str, Any]]: Lista de diccionarios con los libros extraídos y validados.
    """
    # Crear archivo temporal para la salida JSON si no se especificó uno
    if archivo_salida:
        salida_json = archivo_salida
        eliminar_al_terminar = False
    else:
        fd, salida_json = tempfile.mkstemp(suffix=".json", prefix="cuspide_scraped_")
        os.close(fd)
        eliminar_al_terminar = True

    try:
        # Script en línea para ejecutar Scrapy en un subproceso aislado
        script_ejecucion = (
            "import sys\n"
            "from scrapy.crawler import CrawlerProcess\n"
            "from scrapy.utils.project import get_project_settings\n"
            "from book_manager.scraper.spiders.cuspide_spider import CuspideSpider\n"
            "\n"
            "settings = get_project_settings()\n"
            f"settings.set('FEED_FORMAT', 'json')\n"
            f"settings.set('FEED_URI', r'{salida_json}')\n"
            "settings.set('FEED_OVERWRITE', True)\n"
            "settings.set('LOG_LEVEL', 'WARNING')\n"
            "\n"
            "process = CrawlerProcess(settings)\n"
            f"libros_arg = {repr(libros)}\n"
            f"max_res = {int(max_resultados)}\n"
            "process.crawl(CuspideSpider, libros=libros_arg, max_resultados=max_res)\n"
            "process.start()\n"
        )

        cwd_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )

        env = os.environ.copy()
        src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        env["PYTHONPATH"] = f"{src_path}{os.pathsep}{env.get('PYTHONPATH', '')}"

        # Ejecutar el subproceso utilizando el mismo intérprete de Python activo
        resultado = subprocess.run(
            [sys.executable, "-c", script_ejecucion],
            cwd=cwd_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if resultado.returncode != 0:
            print(f"⚠️ Advertencia en ejecución del scraper: {resultado.stderr.strip()}")

        # Leer los resultados generados en el archivo JSON
        if os.path.exists(salida_json) and os.path.getsize(salida_json) > 0:
            with open(salida_json, mode="r", encoding="utf-8") as f:
                items = json.load(f)
                return items if isinstance(items, list) else []
        return []

    except Exception as e:
        print(f"❌ Error al ejecutar el scraper de Cúspide: {e}")
        return []
    finally:
        if eliminar_al_terminar and os.path.exists(salida_json):
            try:
                os.remove(salida_json)
            except OSError:
                pass
