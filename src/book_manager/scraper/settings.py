"""Configuración del framework Scrapy para Book Manager.

Establece las directivas de ejecución, identificación de agente de usuario,
políticas de descarga y módulos de spiders y pipelines.
"""

import os
import sys

# Asegurar que el directorio src/ esté en el path de búsqueda de módulos de Python
_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

BOT_NAME = "book_manager_scraper"

SPIDER_MODULES = ["book_manager.scraper.spiders"]
NEWSPIDER_MODULE = "book_manager.scraper.spiders"

# Respeto a robots.txt y políticas de cabecera
ROBOTSTXT_OBEY = False

# Agente de usuario simulando navegador de escritorio estándar
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

# Concurrencia y pausas éticas de rastreo
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.0
COOKIES_ENABLED = False

# Registro y codificación
LOG_LEVEL = "WARNING"
FEED_EXPORT_ENCODING = "utf-8"

# Reactor asíncrono y huellas digitales
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Configuración de pipelines activos (validación y almacenamiento en memoria)
ITEM_PIPELINES = {
    "book_manager.scraper.pipelines.ValidacionLibroPipeline": 300,
    "book_manager.scraper.pipelines.AlmacenamientoItemsPipeline": 400,
}
