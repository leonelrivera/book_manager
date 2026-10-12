"""Punto de entrada principal para el sistema Book Manager (Sprint 2).

Orquesta la inicialización de los servicios mediante inyección de dependencias,
la conexión a la base de datos relacional (Supabase PostgreSQL), la migración
opcional de datos y la interfaz de usuario en consola.
"""

import os
import sys
from typing import Optional

from book_manager.database.connection import ConexionDB
from book_manager.migrations.migrations import migrar_datos
from book_manager.repositories.repositories import (
    RepositorioCotizacionDolar,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)
from book_manager.services.services import BookManagerService
from book_manager.ui.console import ConsolaUI


def main(
    import_default_data: bool = False,
    ruta_csv: Optional[str] = None,
    modo_interactivo: Optional[bool] = None,
) -> BookManagerService:
    """Función principal de ejecución del sistema Book Manager (Sprint 2).

    Args:
        import_default_data (bool): Si es True, ejecuta la migración explícita
            de datos desde migrations/csv hacia migrations/sql y la base de datos.
            Si es False, respeta la configuración y NO imprime 'Cargando datos base...'
            ni fuerza la recarga de datos.
        ruta_csv (Optional[str]): Ruta personalizada hacia los archivos CSV (opcional).
        modo_interactivo (Optional[bool]): Si es False, ejecuta la demostración
            automatizada exigida por el notebook de evaluación para Colab.
            Por defecto, detecta automáticamente si el entorno permite input().

    Returns:
        BookManagerService: Instancia del servicio central configurado.
    """
    print("🚀 Inicializando Book Manager - Sprint 2...")

    # 1. Verificación de conectividad a la base de datos relacional
    conexion = ConexionDB.get_instancia()
    conectado = conexion.probar_conexion()
    if conectado:
        print("✅ Conexión con base de datos relacional (PostgreSQL / Supabase) establecida exitosamente.")
    else:
        print("⚠️ Advertencia: No se pudo verificar la conexión con la base de datos relacional.")

    # 2. Inyección de dependencias: Creación explícita de repositorios y servicio central
    repo_libro = RepositorioLibro(conexion)
    repo_genero = RepositorioGenero(conexion)
    repo_editorial = RepositorioEditorial(conexion)
    repo_moneda = RepositorioMoneda(conexion)
    repo_tipo = RepositorioTipoCotizacion(conexion)
    repo_precio = RepositorioPrecio(conexion)
    repo_stock = RepositorioStock(conexion)
    repo_cotizacion = RepositorioCotizacionDolar(conexion)

    bm_service = BookManagerService(
        repo_libro=repo_libro,
        repo_genero=repo_genero,
        repo_editorial=repo_editorial,
        repo_moneda=repo_moneda,
        repo_tipo_cotizacion=repo_tipo,
        repo_precio=repo_precio,
        repo_stock=repo_stock,
        repo_cotizacion=repo_cotizacion,
    )

    # 3. Migración de datos: ÚNICAMENTE si import_default_data es True explícitamente
    # Esto resuelve la observación del profesor en la entrega anterior
    if import_default_data:
        print("📂 Cargando datos base desde migraciones CSV a SQL y base de datos...")
        carpeta_csv = ruta_csv or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "migrations", "csv")
        )
        carpeta_sql = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "migrations", "sql")
        )
        resumen = migrar_datos(carpeta_csv, carpeta_sql)
        print(f"✅ Migración completada exitosamente: {resumen}")

    # 4. Inicialización de la interfaz de consola
    ui = ConsolaUI(bm_service)

    # Detección de entorno interactivo vs notebook Colab
    es_colab = "google.colab" in sys.modules
    no_tty = not sys.stdin.isatty() if hasattr(sys.stdin, "isatty") else True

    if modo_interactivo is False or es_colab or no_tty:
        # Modo demostración y comprobaciones automatizadas para el Notebook de evaluación
        ui.ejecutar_demostracion_completa()
    else:
        # Modo consola interactiva normal
        ui.iniciar_menu_interactivo()

    return bm_service


if __name__ == "__main__":
    forzar_importacion = "--import-data" in sys.argv or "-i" in sys.argv
    es_demo = "--demo" in sys.argv
    main(
        import_default_data=forzar_importacion,
        modo_interactivo=False if es_demo else None,
    )
