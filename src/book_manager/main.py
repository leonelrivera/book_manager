"""Punto de entrada principal para el sistema Book Manager (Sprint 1).

Orquesta la inicialización de los servicios, la carga inicial opcional o
automática de datos desde archivos CSV, y la ejecución de la interfaz de usuario.
"""

import sys
from typing import Optional

from book_manager.preload_data.preload_data import precargar_datos
from book_manager.services.services import BookManagerService
from book_manager.ui.console import ConsolaUI


def main(
    import_default_data: bool = False,
    ruta_csv: Optional[str] = None,
) -> BookManagerService:
    """Función principal de ejecución del sistema Book Manager.

    Args:
        import_default_data (bool): Si es True o si el sistema detecta repositorios vacíos,
                                    importa automáticamente los datos desde migrations/csv.
        ruta_csv (Optional[str]): Ruta personalizada hacia los archivos CSV (opcional).

    Returns:
        BookManagerService: Instancia del servicio central con el estado actual del sistema.
    """
    print("🚀 Inicializando Book Manager - Sprint 1...")

    # 1. Inicialización del orquestador central y repositorios
    bm_service = BookManagerService()

    # 2. Precarga de datos: si se solicita explícitamente o si el catálogo está vacío
    # Esto asegura que main(import_default_data=False) en el Notebook ejecute con datos precargados
    libros_existentes = bm_service.libro_service.listar_todos()
    if import_default_data or len(libros_existentes) == 0:
        print("📂 Cargando datos base desde migraciones CSV...")
        resumen = precargar_datos(bm_service, ruta_csv=ruta_csv)
        print(
            f"✅ Precarga completada exitosamente: {resumen.get('libros', 0)} libros, "
            f"{resumen.get('generos', 0)} géneros, {resumen.get('editoriales', 0)} editoriales, "
            f"{resumen.get('cotizaciones', 0)} cotizaciones."
        )

    # 3. Inicialización de la interfaz de consola
    ui = ConsolaUI(bm_service)

    # 4. Ejecución del menú principal
    ui.iniciar_menu_interactivo()

    return bm_service


if __name__ == "__main__":
    # Flags por línea de comandos: --import-data para forzar recarga
    forzar_importacion = "--import-data" in sys.argv or "-i" in sys.argv
    main(import_default_data=forzar_importacion)
