"""Módulo de migración de datos para Book Manager.

Contiene la lógica de transformación y migración de datos desde archivos planos CSV
hacia sentencias SQL (.sql) y su inserción física en la base de datos relacional
(PostgreSQL / Supabase / SQLite) mediante SQLAlchemy.
"""

import csv
import os
from typing import Any, Dict, List, Optional
from sqlalchemy import text
from book_manager.database.connection import ConexionDB


def _escapar_sql_valor(valor: Any) -> str:
    """Escapa y formatea un valor para una sentencia INSERT de SQL estándar.

    Args:
        valor: Valor a convertir (str, int, float, None).

    Returns:
        str: Representación en sintaxis SQL ('NULL', 'texto', o numérico).
    """
    if valor is None:
        return "NULL"
    val_str = str(valor).strip()
    if val_str == "" or val_str.upper() == "NULL":
        return "NULL"
    # Verificar si es numérico (entero o flotante)
    try:
        if "." in val_str:
            float(val_str)
            return val_str
        int(val_str)
        return val_str
    except ValueError:
        pass
    # Es cadena de texto: escapar comillas simples duplicándolas
    escapado = val_str.replace("'", "''")
    return f"'{escapado}'"


def generar_insert_sql(tabla: str, columnas: List[str], filas: List[Dict[str, Any]]) -> str:
    """Genera las sentencias SQL de inserción para una tabla específica.

    Args:
        tabla: Nombre de la tabla de destino.
        columnas: Lista de nombres de columnas.
        filas: Lista de diccionarios con los datos leídos del CSV.

    Returns:
        str: Contenido del script SQL con sentencias INSERT.
    """
    if not filas:
        return f"-- Sin datos para la tabla {tabla}\n"

    lineas = [f"-- Migración de datos para la tabla: {tabla}", f"-- Total de registros: {len(filas)}", ""]
    cols_str = ", ".join(columnas)

    for fila in filas:
        valores = [_escapar_sql_valor(fila.get(col)) for col in columnas]
        val_str = ", ".join(valores)
        lineas.append(f"INSERT INTO {tabla} ({cols_str}) VALUES ({val_str});")

    lineas.append("")
    return "\n".join(lineas)


def migrar_datos(carpeta_csvs: str, carpeta_sqls: str) -> Dict[str, int]:
    """Función encargada de la migración de datos de csv a sql.

    Se encarga de leer los archivos csv y crear los archivos sql
    para la inserción en la base de datos, además de poblar la base de datos
    utilizando SQLAlchemy respetando el orden de dependencias referenciales.

    Args:
        carpeta_csvs (str): Carpeta donde se encuentran los archivos csv de origen.
        carpeta_sqls (str): Carpeta donde se deben guardar los archivos sql generados.

    Returns:
        Dict[str, int]: Diccionario con el conteo de registros migrados por tabla.
    """
    os.makedirs(carpeta_sqls, exist_ok=True)

    # Orden estricto de dependencias referenciales
    orden_tablas = [
        ("generos.csv", "generos", ["id", "nombre", "descripcion"]),
        ("editoriales.csv", "editoriales", ["id", "nombre", "pais", "contacto"]),
        ("monedas.csv", "monedas", ["id", "codigo", "nombre", "simbolo"]),
        ("tipos_cotizacion.csv", "tipos_cotizacion", ["id", "nombre", "descripcion"]),
        ("libros.csv", "libros", ["id", "isbn", "titulo", "autor", "anio_publicacion", "paginas", "id_genero", "id_editorial"]),
        ("precios.csv", "precios", ["id", "id_libro", "id_moneda", "valor"]),
        ("stock.csv", "stock", ["id", "id_libro", "cantidad", "ubicacion"]),
        ("cotizaciones.csv", "cotizaciones", ["id", "id_tipo", "fecha", "compra", "venta"]),
    ]

    resumen: Dict[str, int] = {}
    conexion = ConexionDB.get_instancia()

    # 1. Lectura de CSVs y generación de archivos .sql
    datos_por_tabla: Dict[str, List[Dict[str, Any]]] = {}

    for archivo_csv, tabla, columnas in orden_tablas:
        ruta_csv = os.path.join(carpeta_csvs, archivo_csv)
        filas: List[Dict[str, Any]] = []

        if os.path.exists(ruta_csv):
            with open(ruta_csv, mode="r", encoding="utf-8") as f:
                lector = csv.DictReader(f)
                filas = [dict(r) for r in lector]
        else:
            print(f"⚠️ Archivo CSV no encontrado: {ruta_csv}")

        datos_por_tabla[tabla] = filas

        # Generar archivo .sql correspondiente
        contenido_sql = generar_insert_sql(tabla, columnas, filas)
        ruta_sql = os.path.join(carpeta_sqls, f"{tabla}.sql")
        with open(ruta_sql, mode="w", encoding="utf-8") as f:
            f.write(contenido_sql)

    # 2. Inserción física en la base de datos mediante SQLAlchemy
    with conexion.obtener_sesion() as session:
        for _, tabla, columnas in orden_tablas:
            filas = datos_por_tabla.get(tabla, [])
            insertados = 0

            for fila in filas:
                cols_presentes = [col for col in columnas if col in fila and fila[col] is not None and str(fila[col]).strip() != ""]
                if not cols_presentes:
                    continue

                cols_clause = ", ".join(cols_presentes)
                params_clause = ", ".join([f":{col}" for col in cols_presentes])

                # Mapear valores con tipos de datos correctos
                valores_dict: Dict[str, Any] = {}
                for col in cols_presentes:
                    val = fila[col]
                    val_str = str(val).strip()
                    if col in ("id", "id_genero", "id_editorial", "id_libro", "id_moneda", "id_tipo", "anio_publicacion", "paginas", "cantidad"):
                        try:
                            valores_dict[col] = int(val_str)
                        except ValueError:
                            valores_dict[col] = None
                    elif col in ("valor", "compra", "venta"):
                        try:
                            valores_dict[col] = float(val_str)
                        except ValueError:
                            valores_dict[col] = 0.0
                    else:
                        valores_dict[col] = val_str

                # Sentencia SQL compatible con SQLite y PostgreSQL (ON CONFLICT DO NOTHING para evitar duplicados en re-ejecución)
                sql_insert = text(
                    f"INSERT INTO {tabla} ({cols_clause}) VALUES ({params_clause}) "
                    f"ON CONFLICT (id) DO NOTHING"
                )

                try:
                    resultado = session.execute(sql_insert, valores_dict)
                    if resultado.rowcount > 0:
                        insertados += 1
                except Exception as e:
                    print(f"Error insertando en {tabla}: {e}")

            resumen[tabla] = insertados

        # Ajustar secuencias en PostgreSQL si el motor es postgresql
        if "postgresql" in str(conexion.engine.url):
            for _, tabla, _ in orden_tablas:
                try:
                    seq_query = text(
                        f"SELECT setval(pg_get_serial_sequence('{tabla}', 'id'), "
                        f"COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM {tabla};"
                    )
                    session.execute(seq_query)
                except Exception:
                    pass

    return resumen
