# Book Manager - Sprint 1

## 📌 Objetivo
Desarrollar una aplicación de consola (CLI) robusta en Python que permita gestionar el inventario de una librería, cotizar los libros en tiempo real según el valor del dólar y administrar la información del catálogo aplicando conceptos de Programación Orientada a Objetos (POO) y persistencia en archivos.

---

## 📖 Introducción y Contexto del Sprint de Trabajo
Una librería con venta al público necesita modernizar su sistema de gestión de inventario de libros. Debido a la fluctuación en los costos de importación de material bibliográfico, el sistema debe gestionar precios en diferentes monedas y seguir de cerca la cotización del dólar para actualizar sus valores en tiempo real.

Tomando como dominio de referencia el catálogo del portal comercial de libros **Cúspide** (*www.cuspide.com*), se modelan y gestionan las siguientes entidades del sistema:

* **Libro:** Representa cada título del catálogo (ISBN, título, autor, género, editorial, año, páginas).
* **Género:** Categoría literaria a la que pertenece un libro (Novela, Cuento, Ensayo, Ciencia Ficción, Historia, etc.).
* **Editorial:** Proveedor o distribuidora que abastece a la librería (Sudamericana, Planeta, Penguin Random House, etc.).
* **Moneda:** Divisas en las que se expresan los precios (ARS, USD, EUR, etc.).
* **TipoCotizacion:** Modalidades de cotización del dólar (Oficial, Blue, MEP, CCL, Tarjeta, etc.).
* **Precio:** Valor monetario asignado a un libro en una moneda determinada.
* **Stock:** Cantidad física disponible y ubicación de cada ejemplar.
* **CotizacionDolar:** Registro histórico y diario de cotizaciones con valores de compra y venta.

