[Ejercicio 5]
* Implementación de la generación de reportes analíticos de precios en formato Excel (`.xlsx`) mediante la librería `openpyxl`:
  - Método `generar_reporte_excel()` en `ComparadorPreciosService` y su delegación en `ReporteService.generar_reporte_excel_precios()` dentro de `src/book_manager/services/services.py`.
  - Inclusión estricta de los campos requeridos por la consigna: `Libro`, `Precio interno`, `Precio web`, `Diferencia` y `Fecha de extracción`.
  - Almacenamiento predeterminado en el directorio de salida del proyecto: `src/book_manager/reportes/reporte_precios.xlsx`.
* Integración en la interfaz de consola `ConsolaUI` (`src/book_manager/ui/console.py`):
  - Nuevo método `generar_reporte_excel_precios()` con notificación de estado, detalle de campos e instrucciones de apertura/descarga.
  - Adición de la opción "7. 📑 Generar Reporte de Precios en Excel (.xlsx con openpyxl)" en el Menú de Reportes Analíticos.
  - Inclusión del reporte en la suite de comprobaciones automatizadas `ejecutar_demostracion_completa()` para su validación en entornos desatendidos (Google Colab).

[Ejercicio 4]
* Implementación del servicio de comparación de precios y generación de alertas de mercado (`ComparadorPreciosService`) en `src/book_manager/services/services.py`:
  - Comparación sistemática entre el precio interno del catálogo (en Pesos Argentinos - ARS) y el precio extraído desde la web del competidor (Cúspide Libros).
  - Selección optimizada del mejor match por cada libro del catálogo (`difflib.SequenceMatcher`), garantizando una única fila representativa por obra y eliminando alertas duplicadas de múltiples ediciones.
  - Cálculo de diferencias nominales y porcentuales entre precios, determinando el tipo de alerta (`COMPETIDOR MÁS CARO`, `COMPETIDOR MÁS BARATO`, `PRECIOS IGUALES`, `SIN PRECIO INTERNO`, `SIN PRECIO WEB`).
  - Activación de alertas de precio en función de un umbral mínimo de diferencia configurable, solicitado al usuario antes de cada ejecución del proceso.
  - Generación automática de archivo descargable en formato CSV (`src/book_manager/reportes/alertas_precios.csv`) con columnas estructuradas para análisis analítico (`isbn`, `titulo_interno`, `titulo_competidor`, `precio_interno`, `precio_web`, `diferencia`, `diferencia_porcentual`, `alerta_activa`, `tipo_alerta`, `detalle_alerta`, `formas_pago`, `url_libro`, `fecha_extraccion`).

[Ejercicio 3]
* Implementación del spider `CuspideSpider` (`src/book_manager/scraper/spiders/cuspide_spider.py`) utilizando el framework Scrapy:
  - Extracción automatizada desde el catálogo web de Cúspide Libros (WooCommerce) de los campos requeridos: precio actual, URL de la imagen de portada, formas de pago y cuotas, descripción detallada/sinopsis y autor competidor.
  - Filtrado y acotamiento estricto a los libros existentes en el catálogo propio, inyectando título y autor interno en la metadata de navegación.
  - Limitación paramétrica de hasta los 10 primeros resultados por cada búsqueda de título.
* Implementación y refinamiento de procesadores de carga con `LibroCompetidorLoader` (`src/book_manager/scraper/loaders.py`) para limpieza de espacios, normalización numérica de precios decimales, procesamiento de autores y combinación estructurada de descripciones y formas de pago.
* Implementación de pipelines de procesamiento (`src/book_manager/scraper/pipelines.py`):
  - `ValidacionLibroPipeline`: Validación semántica de coincidencia de título y autor (descartando con `DropItem` obras que no pertenezcan al autor buscado o títulos ajenos como falsos positivos del buscador web), descarte de registros con precios inválidos o nulos e imputación de valores por defecto coherentes.
  - `AlmacenamientoItemsPipeline`: Recolección en memoria de los ítems validados durante la sesión de rastreo.
* Creación del módulo ejecutor `runner.py` (`src/book_manager/scraper/runner.py`) con la función `ejecutar_scraper()`, aislando la ejecución de Twisted en subprocesos para permitir llamadas reiteradas sin errores `ReactorNotRestartable`.
* Creación de `scrapy.cfg` en la raíz del proyecto para integración con la CLI estándar de Scrapy.

[Ejercicio 2]
* Implementación de la función `cargar_datos_desde_sql(ruta_origen, conexion)` en `src/book_manager/preload_data/preload_data.py`:
  - Lectura estructurada y ejecución directa de scripts `.sql` respetando el orden estricto de dependencias e integridad referencial (`generos`, `editoriales`, `monedas`, `tipos_cotizacion`, `libros`, `precios`, `stock` y `cotizaciones`).
  - Integración del método `cargar_desde_sql()` en la clase `PrecargaDatos` y exportación centralizada en `src/book_manager/preload_data/__init__.py`.

[Ejercicio 1]
* Inicialización y configuración de la herramienta de versionado en la rama `Sprint_3` partiendo de la rama `Sprint_2`.
* Configuración de la estructura de directorios establecida para el Sprint 3:
  - Creación del paquete `src/book_manager/scraper/` con los componentes arquitectónicos de Scrapy: configuración (`settings.py`), modelo de datos de competidores (`items.py`), cargadores y procesadores de limpieza (`loaders.py`), pipelines de validación (`pipelines.py`) y subpaquete de spiders (`spiders/`).
  - Creación y seguimiento en Git del directorio `src/book_manager/reportes/` (`.gitkeep`) destinado a la generación de reportes en hojas de cálculo Excel.
  - Creación del módulo de inicialización de paquete `__init__.py` en `src/book_manager/preload_data/`.
* Actualización de dependencias del proyecto en `requirements.txt`, incorporando `scrapy` (extracción web automatizada de catálogos de la competencia) y `openpyxl` (generación y formateo de reportes en Excel).
* Actualización integral del archivo `README.md` detallando objetivos comerciales, alcance e introducción al contexto de trabajo del Sprint 3.

[Correcciones TP02]
* Incorporación de mensaje explícito por consola en `ConexionDB` (`src/book_manager/database/connection.py`) cuando no se detecta `DATABASE_URL` en el entorno y se recurre a SQLite como fallback.
* Adición de restricción `UniqueConstraint("id_tipo", "fecha", name="uq_cotizacion_tipo_fecha")` en `CotizacionDolarModel` (`src/book_manager/models/models.py`), preservando la clave primaria autoincremental y garantizando unicidad de cotizaciones por fecha y tipo.
* Eliminación de URL por defecto hardcodeada en `CotizacionService.obtener_cotizaciones()` (`src/book_manager/services/services.py`), requiriendo estrictamente `API_URL` del archivo `.env`.
* Manejo y distinción de excepciones de red específicas con `requests` (`Timeout`, `ConnectionError`, `HTTPError`, `RequestException`, `ValueError`).

[Ejercicio 8]
* Incorporación de las nuevas opciones del menú de consola en `src/book_manager/ui/console.py`:
  - Opción para descarga y sincronización de cotizaciones en tiempo real mediante DolarAPI (`obtener_cotizaciones_por_api()`).
  - Opción para visualización de la lista de precios bimonetaria de los libros (ARS y moneda seleccionada según cotización vigente, por defecto Dólar Blue: `ver_precios_bimonetarios()`).
  - Opción para exportación integral de la lista de precios a archivo CSV multi-cotización (`exportar_precios_csv()` hacia `migrations/csv/exportacion_precios.csv`).
* Adaptación del menú interactivo por consola mediante coincidencia de patrones (`match-case`), incluyendo submenús dedicados y opción de auto-demostración (`ejecutar_demostracion_completa()`).
* Actualización de `main.py` para soportar ejecución desatendida/automatizada (Google Colab / "Ejecutar todo") y corrección de la observación del TP01 (evitando imprimir "Cargando datos base..." si `import_default_data=False`).

[Ejercicio 7]
* Implementación de la función `obtener_cotizaciones()` en `CotizacionService` (alias `ServicioCotizacionDolar`) dentro de `src/book_manager/services/services.py`.
* Integración con la API externa `DolarAPI` (`https://dolarapi.com/v1/dolares`) configurada de forma segura mediante la variable de entorno `API_URL` en `.env`.
* Descarga, normalización y persistencia en tiempo real de cotizaciones para todas las casas de cambio (Oficial, Blue, Bolsa, Contado con liquidación, Mayorista, Cripto, Tarjeta) en la base de datos de Supabase.
* Refactorización de `BookManagerService` incorporando Inyección de Dependencias modular (permitiendo inicializar repositorios de forma independiente, subsanando la observación del TP01).

[Ejercicio 6]
* Refactorización integral de la capa de repositorios en `src/book_manager/repositories/repositories.py` para operar sobre la base de datos relacional con SQLAlchemy 2.0.
* Adaptación de la clase genérica `RepositorioBase[T, M]` con operaciones CRUD transaccionales (`session.get`, `session.add`, `session.delete`, `select`).
* Conversión transparente bidireccional entre modelos ORM (`models.py`) y entidades de dominio (`entities.py`), preservando la composición y navegación orientada a objetos pura (`libro.genero`, `libro.editorial`).
* Implementación de validaciones de integridad referencial para prevenir borrados inseguros de géneros, editoriales o monedas con registros dependientes (subsanando la observación de la devolución del TP01).
* Métodos de búsqueda especializados sobre la base de datos (por ISBN, título, autor, código de moneda, cotizaciones históricas y stock por libro).

[Ejercicio 5]
* Implementación de la función `migrar_datos(carpeta_csvs, carpeta_sqls)` en `src/book_manager/migrations/migrations.py`.
* Lectura estructurada de los archivos CSV de Sprint 1 respetando el orden estricto de dependencias e integridad referencial.
* Generación automatizada de los scripts `.sql` con sentencias `INSERT INTO` en `src/book_manager/migrations/sql/` para cada una de las 8 tablas.
* Población física exitosa de la base de datos PostgreSQL en Supabase con cláusulas de prevención de duplicados (`ON CONFLICT DO NOTHING`) y actualización de secuencias.

[Ejercicio 4]
* Definición de los modelos relacionales ORM en `src/book_manager/models/models.py` utilizando `DeclarativeBase` de SQLAlchemy 2.0.
* Mapeo de tablas: `generos`, `editoriales`, `monedas`, `tipos_cotizacion`, `libros`, `precios`, `stock` y `cotizaciones`.
* Configuración de claves primarias autoincrementales, restricciones de unicidad e integridad referencial (`ForeignKey` con cascada controlada).
* Implementación de relaciones bidireccionales con `relationship()`, permitiendo navegación orientada a objetos pura (`libro.genero`, `libro.editorial`, `precio.moneda`, `stock.libro`).
* Creación física y verificación de esquemas relacionales en la base de datos PostgreSQL de Supabase.

[Ejercicio 3]
* Implementación de gestores de contexto (Context Managers) para transacciones atómicas con la base de datos en `src/book_manager/database/connection.py`.
* Creación de la clase `TransaccionContextManager` con protocolo estándar `__enter__` y `__exit__`, controlando commit automático, rollback ante excepciones y cierre seguro (`close`) de la sesión.
* Implementación del método generador `@contextmanager` `obtener_sesion()` en la clase `ConexionDB`.
* Función de utilidad global `transaccion_db()` para simplificar operaciones transaccionales seguras en repositorios y servicios.

[Ejercicio 2]
* Implementación de la clase `ConexionDB` en `src/book_manager/database/connection.py` para la gestión centralizada de la base de datos relacional.
* Integración con SQLAlchemy 2.0 (`create_engine`, `sessionmaker`) y soporte para Supabase (PostgreSQL) con compatibilidad de variables de entorno mediante `python-dotenv`.
* Métodos de obtención de motor, creación de sesiones y verificación de conectividad mediante `probar_conexion()`.

[Ejercicio 1]
* Inicialización de la rama de trabajo `Sprint_2` partiendo de `Sprint_1`.
* Creación y configuración de la nueva estructura de directorios: paquetes `database/`, `models/` y carpeta de migraciones `migrations/sql/`.
* Creación del archivo de configuración de variables de entorno `.env` con endpoints y cadenas de conexión a base de datos.
* Actualización de dependencias en `requirements.txt` incorporando `SQLAlchemy`, `python-dotenv`, `requests` y `psycopg2-binary`.
* Actualización de `README.md` detallando objetivos, alcance y contexto técnico del Sprint 2.

[Punto 7]
* Creación e implementación del punto de entrada principal `main.py`.

[Punto 6]
* Implementación de la interfaz de usuario en consola (`src/book_manager/ui/console.py`) con la clase `ConsolaUI`.
* Métodos formateados para operaciones CRUD de cada entidad (Libro, Género, Editorial, Moneda, Tipo de Cotización, Precios, Stock y Cotizaciones de Dólar).
* Método `ejecutar_demostracion_completa()` para la ejecución secuencial automatizada exigida en las validaciones de la entrega.

[Punto 5]
* Creación de archivos de migración CSV dentro de `src/book_manager/migrations/csv/` con un mínimo de 10 registros reales por entidad basados en el catálogo de Cúspide: `generos.csv`, `editoriales.csv`, `monedas.csv`, `tipos_cotizacion.csv`, `libros.csv`, `precios.csv`, `stock.csv` y `cotizaciones.csv`.

[Ejercicio 4]
* Implementación de la capa de servicios y lógica de negocio: `LibroService`, `GeneroService`, `EditorialService`, `MonedaService`, `TipoCotizacionService`, `CotizacionService`, `StockService` y `PrecioService`.
* Implementación de motor de conversión multimoneda (ARS/USD) considerando tipos de cotización del dólar (Oficial, Blue, MEP).
* Lógica para el control de inventario, actualización de existencias y control de stock mínimo.
* Creación de `ReporteService` para catálogos completos con conversión de divisas, valorización total del inventario y alertas de stock crítico.

[Ejercicio 3]
* Implementación de la clase genérica `RepositorioBase[T]` con operaciones CRUD completas (crear, leer por ID, leer todos, actualizar, eliminar).
* Creación de repositorios concretos para cada entidad: `RepositorioLibro`, `RepositorioGenero`, `RepositorioEditorial`, `RepositorioMoneda`, `RepositorioTipoCotizacion`, `RepositorioPrecio`, `RepositorioStock` y `RepositorioCotizacionDolar`.
* Métodos de búsqueda especializados (búsqueda por ISBN, título, autor, género, histórico de cotizaciones y stock por libro).

[Ejercicio 2]
* Implementación de entidades de dominio: `Libro`, `Genero`, `Editorial`, `Moneda`, `TipoCotizacion`, `Precio`, `Stock` y `CotizacionDolar`.
* Aplicación de encapsulamiento estricto mediante atributos privados y `@property` con validaciones de tipos y valores.
* Incorporación de métodos de serialización (`to_dict`, `from_dict`) y representación (`__repr__`).

[Ejercicio 1]
* Creación de rama Sprint_1 y archivos base.
* Configuración de la estructura de directorios (`src/book_manager/...`).
