"""Módulo para la precarga e importación de datos iniciales desde archivos CSV.

Permite poblar el catálogo y configurar la persistencia activa en los archivos CSV
ubicados en migrations/csv respetando las relaciones y composición de objetos.
"""

import csv
import os
from typing import Optional

from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from book_manager.services.services import BookManagerService


class PrecargaDatos:
    """Clase encargada de cargar los archivos CSV y vincular la persistencia en disco."""

    def __init__(self, book_manager_service: BookManagerService, ruta_csv: Optional[str] = None) -> None:
        self._bm = book_manager_service
        if ruta_csv:
            self._ruta_csv = ruta_csv
        else:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            self._ruta_csv = os.path.abspath(
                os.path.join(directorio_actual, "..", "migrations", "csv")
            )

        # Vincular las rutas de los archivos CSV a los repositorios para auto-guardado activo
        self._configurar_rutas_repositorios()

    def _obtener_ruta_archivo(self, nombre_archivo: str) -> str:
        ruta_completa = os.path.join(self._ruta_csv, nombre_archivo)
        if not os.path.exists(ruta_completa):
            rutas_alternativas = [
                os.path.join(os.getcwd(), "src", "book_manager", "migrations", "csv", nombre_archivo),
                os.path.join(os.getcwd(), "book_manager", "migrations", "csv", nombre_archivo),
                os.path.join("/content", "book_manager", "src", "book_manager", "migrations", "csv", nombre_archivo),
            ]
            for alt in rutas_alternativas:
                if os.path.exists(alt):
                    return alt
        return ruta_completa

    def _configurar_rutas_repositorios(self) -> None:
        self._bm.repo_genero.set_archivo_csv(self._obtener_ruta_archivo("generos.csv"))
        self._bm.repo_editorial.set_archivo_csv(self._obtener_ruta_archivo("editoriales.csv"))
        self._bm.repo_moneda.set_archivo_csv(self._obtener_ruta_archivo("monedas.csv"))
        self._bm.repo_tipo_cotizacion.set_archivo_csv(self._obtener_ruta_archivo("tipos_cotizacion.csv"))
        self._bm.repo_cotizacion.set_archivo_csv(self._obtener_ruta_archivo("cotizaciones.csv"))
        self._bm.repo_libro.set_archivo_csv(self._obtener_ruta_archivo("libros.csv"))
        self._bm.repo_precio.set_archivo_csv(self._obtener_ruta_archivo("precios.csv"))
        self._bm.repo_stock.set_archivo_csv(self._obtener_ruta_archivo("stock.csv"))

    def _leer_archivo_csv(self, nombre_archivo: str) -> list:
        ruta = self._obtener_ruta_archivo(nombre_archivo)
        if not os.path.exists(ruta):
            print(f"⚠️ Advertencia: No se encontró el archivo '{nombre_archivo}' en {self._ruta_csv}.")
            return []

        registros = []
        with open(ruta, mode="r", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                registros.append(fila)
        return registros

    def cargar_generos(self) -> int:
        filas = self._leer_archivo_csv("generos.csv")
        cargados = 0
        for fila in filas:
            try:
                genero = Genero.from_dict(fila)
                self._bm.repo_genero.crear(genero)
                cargados += 1
            except Exception as e:
                print(f"Error cargando género {fila}: {e}")
        return cargados

    def cargar_editoriales(self) -> int:
        filas = self._leer_archivo_csv("editoriales.csv")
        cargados = 0
        for fila in filas:
            try:
                editorial = Editorial.from_dict(fila)
                self._bm.repo_editorial.crear(editorial)
                cargados += 1
            except Exception as e:
                print(f"Error cargando editorial {fila}: {e}")
        return cargados

    def cargar_monedas(self) -> int:
        filas = self._leer_archivo_csv("monedas.csv")
        cargados = 0
        for fila in filas:
            try:
                moneda = Moneda.from_dict(fila)
                self._bm.repo_moneda.crear(moneda)
                cargados += 1
            except Exception as e:
                print(f"Error cargando moneda {fila}: {e}")
        return cargados

    def cargar_tipos_cotizacion(self) -> int:
        filas = self._leer_archivo_csv("tipos_cotizacion.csv")
        cargados = 0
        for fila in filas:
            try:
                tipo = TipoCotizacion.from_dict(fila)
                self._bm.repo_tipo_cotizacion.crear(tipo)
                cargados += 1
            except Exception as e:
                print(f"Error cargando tipo cotización {fila}: {e}")
        return cargados

    def cargar_cotizaciones(self) -> int:
        filas = self._leer_archivo_csv("cotizaciones.csv")
        cargados = 0
        for fila in filas:
            try:
                cot = CotizacionDolar.from_dict(fila)
                self._bm.repo_cotizacion.crear(cot)
                cargados += 1
            except Exception as e:
                print(f"Error cargando cotización {fila}: {e}")
        return cargados

    def cargar_libros(self) -> int:
        filas = self._leer_archivo_csv("libros.csv")
        cargados = 0
        for fila in filas:
            try:
                # Cargar objeto Género y objeto Editorial para composición POO pura
                id_gen = int(fila["id_genero"])
                id_ed = int(fila["id_editorial"])
                genero_obj = self._bm.repo_genero.leer_por_id(id_gen) or id_gen
                editorial_obj = self._bm.repo_editorial.leer_por_id(id_ed) or id_ed

                libro = Libro(
                    id_libro=int(fila["id"]) if fila.get("id") else None,
                    isbn=str(fila["isbn"]),
                    titulo=str(fila["titulo"]),
                    autor=str(fila["autor"]),
                    genero=genero_obj,
                    editorial=editorial_obj,
                    anio_publicacion=int(fila["anio_publicacion"]) if fila.get("anio_publicacion") else None,
                    paginas=int(fila["paginas"]) if fila.get("paginas") else None,
                )
                self._bm.repo_libro.crear(libro)
                cargados += 1
            except Exception as e:
                print(f"Error cargando libro {fila}: {e}")
        return cargados

    def cargar_precios(self) -> int:
        filas = self._leer_archivo_csv("precios.csv")
        cargados = 0
        for fila in filas:
            try:
                precio = Precio.from_dict(fila)
                self._bm.repo_precio.crear(precio)
                cargados += 1
            except Exception as e:
                print(f"Error cargando precio {fila}: {e}")
        return cargados

    def cargar_stock(self) -> int:
        filas = self._leer_archivo_csv("stock.csv")
        cargados = 0
        for fila in filas:
            try:
                stock = Stock.from_dict(fila)
                self._bm.repo_stock.crear(stock)
                cargados += 1
            except Exception as e:
                print(f"Error cargando stock {fila}: {e}")
        return cargados

    def cargar_todo(self) -> dict:
        """Carga todas las entidades respetando el orden de dependencias relacionales."""
        resumen = {
            "generos": self.cargar_generos(),
            "editoriales": self.cargar_editoriales(),
            "monedas": self.cargar_monedas(),
            "tipos_cotizacion": self.cargar_tipos_cotizacion(),
            "cotizaciones": self.cargar_cotizaciones(),
            "libros": self.cargar_libros(),
            "precios": self.cargar_precios(),
            "stock": self.cargar_stock(),
        }
        return resumen


def precargar_datos(book_manager_service: BookManagerService, ruta_csv: Optional[str] = None) -> dict:
    """Función helper para ejecutar la precarga completa de datos desde CSV."""
    cargador = PrecargaDatos(book_manager_service, ruta_csv)
    return cargador.cargar_todo()
