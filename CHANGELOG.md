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
