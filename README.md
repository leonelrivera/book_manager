# Book Manager - Sprint 3

## 📌 Objetivo
El objetivo principal de este sprint es incorporar la descarga y obtención automatizada de datos desde la web (Web Scraping) para recopilar información de precios de competidores (librerías con venta online como Cúspide), permitiendo comparar dichos valores con nuestro catálogo interno y competir de forma informada. Asimismo, se busca generar reportes analíticos avanzados en formato Excel (.xlsx), archivos de alertas de precios (CSV) y dotar al sistema de mecanismos de auditoría mediante decoradores para el registro y trazabilidad de todas las operaciones realizadas.

---

## 📖 Introducción y Contexto del Sprint de Trabajo
En esta tercera entrega del proyecto integrador, la librería avanza hacia la inteligencia comercial y el monitoreo de mercado mediante la extracción automatizada de datos web. Partiendo de la base de datos relacional y servicios consolidados en el Sprint 2, se integran las siguientes capacidades:

* **Web Scraping con Scrapy:** Implementación de spiders (`CuspideSpider`), loaders y pipelines para la búsqueda automatizada y estructurada de precios, imágenes, descripciones y formas de pago de los libros existentes en el catálogo.
* **Carga Inicial SQL:** Incorporación de mecanismos de precarga directa de datos desde sentencias SQL relacionales.
* **Comparativa de Precios y Sistema de Alertas:** Lógica de comparación entre precios internos y precios de la competencia en la web, con umbrales de diferencia parametrizables por el usuario y generación de alertas en formato CSV.
* **Reportes Analíticos en Excel:** Exportación de reportes detallados en hojas de cálculo `.xlsx` (vía `openpyxl`) para análisis de discrepancias de precios y fechas de extracción.
* **Módulo de Auditoría Transaccional:** Registro sistemático de cada operación del sistema (acción, fecha, detalles) mediante la aplicación de decoradores de Python (`@auditar`) persistidos en la base de datos.
* **Interfaz de Consola Extendida:** Incorporación de nuevas opciones interactivas en el menú de usuario para ejecutar scraping, emitir reportes y consultar el historial de auditoría.
