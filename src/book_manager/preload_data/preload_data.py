"""Módulo para la precarga e importación de datos iniciales en Book Manager.

Proporciona soporte para la carga inicial de datos desde archivos planos CSV
y la ejecución directa de sentencias SQL estructuradas (.sql) en la base de datos
relacional respetando las relaciones y la integridad referencial.
"""

import csv
import os
import re
from typing import Dict, List, Optional
from sqlalchemy import text

from book_manager.database.connection import ConexionDB
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


ORDEN_TABLAS_SQL: List[str] = [
    "generos",
    "editoriales",
    "monedas",
    "tipos_cotizacion",
    "libros",
    "precios",
    "stock",
    "cotizaciones",
]


class PrecargaDatos:
    """Clase encargada de cargar los datos iniciales y vincular la persistencia."""

    def __init__(self, book_manager_service: BookManagerService, ruta_csv: Optional[str] = None) -> None:
        """Inicializa la precarga de datos vinculando el servicio y las rutas.

        Args:
            book_manager_service: Servicio principal de Book Manager.
            ruta_csv: Ruta opcional hacia la carpeta de archivos CSV.
        """
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
        """Obtiene la ruta absoluta a un archivo verificando ubicaciones alternativas."""
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

    def _configurar_rutas_repositorios() -> None:
        pass

    def _configurar_rutas_repositorios(self) -> None:
        """Configura los archivos CSV asociados a cada repositorio si corresponde."""
        for repo_attr, archivo in [
            ("repo_genero", "generos.csv"),
            ("repo_editorial", "editoriales.csv"),
            ("repo_moneda", "monedas.csv"),
            ("repo_tipo_cotizacion", "tipos_cotizacion.csv"),
            ("repo_cotizacion", "cotizaciones.csv"),
            ("repo_libro", "libros.csv"),
            ("repo_precio", "precios.csv"),
            ("repo_stock", "stock.csv"),
        ]:
            repo = getattr(self._bm, repo_attr, None)
            if repo and hasattr(repo, "set_archivo_csv"):
                repo.set_archivo_csv(self._obtener_ruta_archivo(archivo))

    def _leer_archivo_csv(self, nombre_archivo: str) -> list:
        """Lee un archivo CSV y retorna una lista de diccionarios por fila."""
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
        """Carga los géneros literarios desde el archivo CSV correspondiente."""
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
        """Carga las editoriales desde el archivo CSV correspondiente."""
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
        """Carga las monedas del sistema desde el archivo CSV correspondiente."""
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
        """Carga los tipos de cotización desde el archivo CSV correspondiente."""
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
        """Carga las cotizaciones del dólar desde el archivo CSV correspondiente."""
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
        """Carga los libros del catálogo vinculando relaciones con género y editorial."""
        filas = self._leer_archivo_csv("libros.csv")
        cargados = 0
        for fila in filas:
            try:
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
        """Carga la lista de precios desde el archivo CSV correspondiente."""
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
        """Carga las existencias de inventario desde el archivo CSV correspondiente."""
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

    def cargar_desde_sql(self, ruta_sql: Optional[str] = None) -> Dict[str, int]:
        """Carga datos directamente desde archivos SQL a la base de datos relacional.

        Args:
            ruta_sql: Ruta opcional a un archivo .sql o directorio de scripts.

        Returns:
            Dict[str, int]: Resumen de inserciones por tabla.
        """
        conexion = getattr(self._bm.repo_libro, "conexion", None)
        return cargar_datos_desde_sql(ruta_origen=ruta_sql, conexion=conexion)


def precargar_datos(book_manager_service: BookManagerService, ruta_csv: Optional[str] = None) -> dict:
    """Función helper para ejecutar la precarga completa de datos desde CSV."""
    cargador = PrecargaDatos(book_manager_service, ruta_csv)
    return cargador.cargar_todo()


def _extraer_sentencias_sql(contenido: str) -> List[str]:
    """Extrae sentencias SQL individuales eliminando comentarios y líneas vacías.

    Args:
        contenido: Texto completo del script SQL.

    Returns:
        List[str]: Lista de sentencias SQL listas para su ejecución.
    """
    lineas_limpias = []
    for linea in contenido.splitlines():
        linea_strip = linea.strip()
        # Omitir comentarios de una sola línea y líneas en blanco
        if linea_strip.startswith("--") or not linea_strip:
            continue
        lineas_limpias.append(linea)

    script_limpio = "\n".join(lineas_limpias)
    sentencias_crudas = script_limpio.split(";")
    sentencias = []
    for s in sentencias_crudas:
        s_strip = s.strip()
        if s_strip:
            sentencias.append(s_strip)
    return sentencias


def cargar_datos_desde_sql(
    ruta_origen: Optional[str] = None,
    conexion: Optional[ConexionDB] = None,
) -> Dict[str, int]:
    """Carga y ejecuta sentencias SQL para poblar la base de datos relacional.

    Lee scripts .sql individuales o un directorio con archivos SQL estructurados
    respetando el orden de dependencias referenciales e integridad relacional.

    Args:
        ruta_origen (Optional[str]): Ruta hacia un archivo .sql específico o hacia
            el directorio que contiene los scripts SQL (por defecto 'migrations/sql').
        conexion (Optional[ConexionDB]): Instancia de ConexionDB para ejecutar
            las sentencias. Si no se especifica, utiliza la instancia Singleton.

    Returns:
        Dict[str, int]: Diccionario con la cantidad de sentencias ejecutadas
            exitosamente por cada tabla o script procesado.
    """
    if conexion is None:
        conexion = ConexionDB.get_instancia()

    # Resolver la ruta de origen por defecto si no fue provista
    if ruta_origen is None:
        candidatos = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "migrations", "sql")),
            os.path.join(os.getcwd(), "src", "book_manager", "migrations", "sql"),
            os.path.join(os.getcwd(), "book_manager", "migrations", "sql"),
            os.path.join("/content", "book_manager", "src", "book_manager", "migrations", "sql"),
        ]
        for c in candidatos:
            if os.path.exists(c):
                ruta_origen = c
                break
        if not ruta_origen or not os.path.exists(ruta_origen):
            ruta_origen = candidatos[0]

    if not os.path.exists(ruta_origen):
        print(f"⚠️ Advertencia: No se encontró la ruta de scripts SQL: {ruta_origen}")
        return {}

    resumen: Dict[str, int] = {}

    with conexion.obtener_sesion() as session:
        # Caso 1: Se pasó un archivo .sql individual
        if os.path.isfile(ruta_origen):
            nombre_tabla = os.path.splitext(os.path.basename(ruta_origen))[0]
            with open(ruta_origen, mode="r", encoding="utf-8") as f:
                sentencias = _extraer_sentencias_sql(f.read())

            insertados = 0
            for sentencia in sentencias:
                sentencia_ejecutar = sentencia
                if re.match(r"(?i)^\s*INSERT\s+INTO", sentencia_ejecutar):
                    if "ON CONFLICT" not in sentencia_ejecutar.upper():
                        sentencia_ejecutar = f"{sentencia_ejecutar} ON CONFLICT (id) DO NOTHING"

                try:
                    res = session.execute(text(sentencia_ejecutar))
                    if res.rowcount is not None and res.rowcount > 0:
                        insertados += res.rowcount
                    else:
                        insertados += 1
                except Exception as e:
                    print(f"Error ejecutando SQL en {nombre_tabla}: {e}")

            resumen[nombre_tabla] = insertados

        # Caso 2: Se pasó un directorio con múltiples archivos .sql
        elif os.path.isdir(ruta_origen):
            # Procesar primero las tablas conocidas en orden de dependencias
            archivos_procesados = set()

            for tabla in ORDEN_TABLAS_SQL:
                nombre_archivo = f"{tabla}.sql"
                ruta_archivo = os.path.join(ruta_origen, nombre_archivo)
                if not os.path.exists(ruta_archivo):
                    continue

                archivos_procesados.add(nombre_archivo)
                with open(ruta_archivo, mode="r", encoding="utf-8") as f:
                    sentencias = _extraer_sentencias_sql(f.read())

                insertados = 0
                for sentencia in sentencias:
                    sentencia_ejecutar = sentencia
                    if re.match(r"(?i)^\s*INSERT\s+INTO", sentencia_ejecutar):
                        if "ON CONFLICT" not in sentencia_ejecutar.upper():
                            sentencia_ejecutar = f"{sentencia_ejecutar} ON CONFLICT (id) DO NOTHING"

                    try:
                        res = session.execute(text(sentencia_ejecutar))
                        if res.rowcount is not None and res.rowcount > 0:
                            insertados += res.rowcount
                        else:
                            insertados += 1
                    except Exception as e:
                        print(f"Error ejecutando SQL en {tabla}: {e}")

                resumen[tabla] = insertados

            # Procesar cualquier otro archivo .sql que pudiera existir en el directorio
            for archivo in sorted(os.listdir(ruta_origen)):
                if archivo.endswith(".sql") and archivo not in archivos_procesados:
                    tabla_extra = os.path.splitext(archivo)[0]
                    ruta_archivo = os.path.join(ruta_origen, archivo)
                    with open(ruta_archivo, mode="r", encoding="utf-8") as f:
                        sentencias = _extraer_sentencias_sql(f.read())

                    insertados = 0
                    for sentencia in sentencias:
                        sentencia_ejecutar = sentencia
                        if re.match(r"(?i)^\s*INSERT\s+INTO", sentencia_ejecutar):
                            if "ON CONFLICT" not in sentencia_ejecutar.upper():
                                sentencia_ejecutar = f"{sentencia_ejecutar} ON CONFLICT (id) DO NOTHING"

                        try:
                            res = session.execute(text(sentencia_ejecutar))
                            if res.rowcount is not None and res.rowcount > 0:
                                insertados += res.rowcount
                            else:
                                insertados += 1
                        except Exception as e:
                            print(f"Error ejecutando SQL en {tabla_extra}: {e}")

                    resumen[tabla_extra] = insertados

        # Ajuste de secuencias seriales si el motor de base de datos es PostgreSQL
        if "postgresql" in str(conexion.engine.url):
            for tabla in ORDEN_TABLAS_SQL:
                try:
                    seq_query = text(
                        f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id'), "
                        f"COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM {tabla};"
                    )
                    session.execute(seq_query)
                except Exception:
                    pass

    print(f"✅ Carga de datos desde SQL completada exitosamente: {resumen}")
    return resumen
