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
