"""Paquete para precarga de datos iniciales en Book Manager.

Proporciona utilidades para la carga inicial mediante archivos CSV o scripts SQL.
"""

from book_manager.preload_data.preload_data import (
    PrecargaDatos,
    cargar_datos_desde_sql,
    precargar_datos,
)

__all__ = ["PrecargaDatos", "cargar_datos_desde_sql", "precargar_datos"]
