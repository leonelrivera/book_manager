"""Capa de servicios y lógica de negocio para el sistema Book Manager.

Contiene los servicios encargados de implementar las reglas de negocio,
conversión de divisas, gestión de stock, orquestación de operaciones CRUD,
integración con APIs externas (DolarAPI) y generación de reportes analíticos.
"""

from datetime import date, datetime
import os
from typing import Any, Dict, List, Optional, Tuple, Union
from dotenv import load_dotenv
import requests

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
from book_manager.repositories.repositories import (
    RepositorioBase,
    RepositorioCotizacionDolar,
    RepositorioEditorial,
    RepositorioGenero,
    RepositorioLibro,
    RepositorioMoneda,
    RepositorioPrecio,
    RepositorioStock,
    RepositorioTipoCotizacion,
)


class GeneroService:
    """Servicio de lógica de negocio para la gestión de Géneros literarios."""

    def __init__(self, repo_genero: RepositorioGenero) -> None:
        self._repo = repo_genero

    def crear_genero(self, nombre: str, descripcion: str = "", id_genero: Optional[int] = None) -> Genero:
        if self._repo.buscar_por_nombre(nombre) is not None:
            raise ValueError(f"Ya existe un género literario con el nombre '{nombre}'.")
        nuevo_genero = Genero(id_genero=id_genero, nombre=nombre, descripcion=descripcion)
        return self._repo.crear(nuevo_genero)

    def obtener_por_id(self, id_genero: int) -> Optional[Genero]:
        return self._repo.leer_por_id(id_genero)

    def obtener_por_nombre(self, nombre: str) -> Optional[Genero]:
        return self._repo.buscar_por_nombre(nombre)

    def listar_todos(self) -> List[Genero]:
        return self._repo.leer_todos()

    def actualizar_genero(self, id_genero: int, nuevo_nombre: str, nueva_descripcion: str = "") -> Genero:
        genero_existente = self._repo.leer_por_id(id_genero)
        if not genero_existente:
            raise ValueError(f"No existe el género con ID {id_genero}.")
        otro_genero = self._repo.buscar_por_nombre(nuevo_nombre)
        if otro_genero and otro_genero.id != id_genero:
            raise ValueError(f"Ya existe otro género con el nombre '{nuevo_nombre}'.")
        genero_existente.nombre = nuevo_nombre
        genero_existente.descripcion = nueva_descripcion
        return self._repo.actualizar(genero_existente)

    def eliminar_genero(self, id_genero: int) -> bool:
        return self._repo.eliminar(id_genero)


class EditorialService:
    """Servicio de lógica de negocio para la gestión de Editoriales."""

    def __init__(self, repo_editorial: RepositorioEditorial) -> None:
        self._repo = repo_editorial

    def crear_editorial(
        self,
        nombre: str,
        pais: str = "Argentina",
        contacto: str = "",
        id_editorial: Optional[int] = None,
    ) -> Editorial:
        if self._repo.buscar_por_nombre(nombre) is not None:
            raise ValueError(f"Ya existe una editorial con el nombre '{nombre}'.")
        nueva_editorial = Editorial(id_editorial=id_editorial, nombre=nombre, pais=pais, contacto=contacto)
        return self._repo.crear(nueva_editorial)

    def obtener_por_id(self, id_editorial: int) -> Optional[Editorial]:
        return self._repo.leer_por_id(id_editorial)

    def obtener_por_nombre(self, nombre: str) -> Optional[Editorial]:
        return self._repo.buscar_por_nombre(nombre)

    def listar_todas(self) -> List[Editorial]:
        return self._repo.leer_todos()

    def actualizar_editorial(
        self,
        id_editorial: int,
        nuevo_nombre: str,
        nuevo_pais: str = "Argentina",
        nuevo_contacto: str = "",
    ) -> Editorial:
        editorial_existente = self._repo.leer_por_id(id_editorial)
        if not editorial_existente:
            raise ValueError(f"No existe la editorial con ID {id_editorial}.")
        otra_editorial = self._repo.buscar_por_nombre(nuevo_nombre)
        if otra_editorial and otra_editorial.id != id_editorial:
            raise ValueError(f"Ya existe otra editorial con el nombre '{nuevo_nombre}'.")
        editorial_existente.nombre = nuevo_nombre
        editorial_existente.pais = nuevo_pais
        editorial_existente.contacto = nuevo_contacto
        return self._repo.actualizar(editorial_existente)

    def eliminar_editorial(self, id_editorial: int) -> bool:
        return self._repo.eliminar(id_editorial)


class MonedaService:
    """Servicio de lógica de negocio para la gestión de Monedas."""

    def __init__(self, repo_moneda: RepositorioMoneda) -> None:
        self._repo = repo_moneda

    def crear_moneda(
        self,
        codigo: str,
        nombre: str,
        simbolo: str = "$",
        id_moneda: Optional[int] = None,
    ) -> Moneda:
        if self._repo.buscar_por_codigo(codigo) is not None:
            raise ValueError(f"Ya existe la moneda con código '{codigo}'.")
        nueva_moneda = Moneda(id_moneda=id_moneda, codigo=codigo, nombre=nombre, simbolo=simbolo)
        return self._repo.crear(nueva_moneda)

    def obtener_por_id(self, id_moneda: int) -> Optional[Moneda]:
        return self._repo.leer_por_id(id_moneda)

    def obtener_por_codigo(self, codigo: str) -> Optional[Moneda]:
        return self._repo.buscar_por_codigo(codigo)

    def listar_todas(self) -> List[Moneda]:
        return self._repo.leer_todos()

    def actualizar_moneda(self, id_moneda: int, codigo: str, nombre: str, simbolo: str = "$") -> Moneda:
        moneda = self._repo.leer_por_id(id_moneda)
        if not moneda:
            raise ValueError(f"No existe la moneda con ID {id_moneda}.")
        otra = self._repo.buscar_por_codigo(codigo)
        if otra and otra.id != id_moneda:
            raise ValueError(f"Ya existe otra moneda con el código '{codigo}'.")
        moneda.codigo = codigo
        moneda.nombre = nombre
        moneda.simbolo = simbolo
        return self._repo.actualizar(moneda)

    def eliminar_moneda(self, id_moneda: int) -> bool:
        return self._repo.eliminar(id_moneda)


class TipoCotizacionService:
    """Servicio de lógica de negocio para los Tipos de Cotización del dólar."""

    def __init__(self, repo_tipo: RepositorioTipoCotizacion) -> None:
        self._repo = repo_tipo

    def crear_tipo(self, nombre: str, descripcion: str = "", id_tipo: Optional[int] = None) -> TipoCotizacion:
        if self._repo.buscar_por_nombre(nombre) is not None:
            raise ValueError(f"Ya existe el tipo de cotización '{nombre}'.")
        nuevo_tipo = TipoCotizacion(id_tipo=id_tipo, nombre=nombre, descripcion=descripcion)
        return self._repo.crear(nuevo_tipo)

    def obtener_por_id(self, id_tipo: int) -> Optional[TipoCotizacion]:
        return self._repo.leer_por_id(id_tipo)

    def obtener_por_nombre(self, nombre: str) -> Optional[TipoCotizacion]:
        return self._repo.buscar_por_nombre(nombre)

    def listar_todos(self) -> List[TipoCotizacion]:
        return self._repo.leer_todos()

    def actualizar_tipo(self, id_tipo: int, nuevo_nombre: str, nueva_descripcion: str = "") -> TipoCotizacion:
        tipo = self._repo.leer_por_id(id_tipo)
        if not tipo:
            raise ValueError(f"No existe el tipo de cotización con ID {id_tipo}.")
        otro = self._repo.buscar_por_nombre(nuevo_nombre)
        if otro and otro.id != id_tipo:
            raise ValueError(f"Ya existe otro tipo de cotización con el nombre '{nuevo_nombre}'.")
        tipo.nombre = nuevo_nombre
        tipo.descripcion = nueva_descripcion
        return self._repo.actualizar(tipo)

    def eliminar_tipo(self, id_tipo: int) -> bool:
        return self._repo.eliminar(id_tipo)


class CotizacionService:
    """Servicio de lógica de negocio para el registro y consulta de cotizaciones del dólar."""

    def __init__(
        self,
        repo_cotizacion: RepositorioCotizacionDolar,
        repo_tipo: RepositorioTipoCotizacion,
    ) -> None:
        self._repo_cotizacion = repo_cotizacion
        self._repo_tipo = repo_tipo

    def registrar_cotizacion(
        self,
        id_tipo: int,
        fecha: Union[date, str],
        compra: float,
        venta: float,
        id_cotizacion: Optional[int] = None,
    ) -> CotizacionDolar:
        tipo = self._repo_tipo.leer_por_id(id_tipo)
        if not tipo:
            raise ValueError(f"El tipo de cotización con ID {id_tipo} no existe.")
        if compra < 0 or venta < 0:
            raise ValueError("Los valores de cotización no pueden ser negativos.")
        if compra > venta:
            raise ValueError("El valor de compra no puede ser mayor que el valor de venta.")

        nueva_cot = CotizacionDolar(
            id_cotizacion=id_cotizacion,
            tipo_cotizacion=tipo,
            fecha=fecha,
            compra=compra,
            venta=venta,
        )
        return self._repo_cotizacion.crear(nueva_cot)

    def obtener_ultima_cotizacion(self, id_tipo: int) -> Optional[CotizacionDolar]:
        return self._repo_cotizacion.leer_ultima_cotizacion(id_tipo)

    def obtener_historico_por_tipo(self, id_tipo: int) -> List[CotizacionDolar]:
        return self._repo_cotizacion.leer_historico_por_tipo(id_tipo)

    def listar_todas(self) -> List[CotizacionDolar]:
        return self._repo_cotizacion.leer_todos()

    def eliminar_cotizacion(self, id_tipo: int, fecha: Union[date, str]) -> bool:
        return self._repo_cotizacion.eliminar(id_tipo, fecha)

    def obtener_cotizaciones(self) -> List[CotizacionDolar]:
        """Busca, descarga y registra las cotizaciones actuales desde la API externa (DolarAPI).

        Lee la URL del endpoint desde la variable de entorno API_URL (.env) y actualiza
        la base de datos con las cotizaciones más recientes de cada casa de cambio.

        Returns:
            List[CotizacionDolar]: Lista de cotizaciones registradas/actualizadas.
        """
        load_dotenv()
        api_url = os.getenv("API_URL", "https://dolarapi.com/v1/dolares")

        try:
            respuesta = requests.get(api_url, timeout=10)
            respuesta.raise_for_status()
            datos = respuesta.json()
        except Exception as e:
            print(f"⚠️ Error al conectar con la API de cotizaciones ({api_url}): {e}")
            return []

        cotizaciones_registradas: List[CotizacionDolar] = []

        for item in datos:
            nombre_tipo = item.get("nombre", "").strip()
            if not nombre_tipo:
                continue

            compra = float(item.get("compra", 0.0) or 0.0)
            venta = float(item.get("venta", 0.0) or 0.0)

            # Normalizar fecha de actualización
            fecha_act_str = item.get("fechaActualizacion", "")
            if fecha_act_str:
                try:
                    fecha_obj = datetime.fromisoformat(fecha_act_str.replace("Z", "+00:00")).date()
                except Exception:
                    fecha_obj = date.today()
            else:
                fecha_obj = date.today()

            # Asegurar existencia del tipo de cotización
            tipo = self._repo_tipo.buscar_por_nombre(nombre_tipo)
            if tipo is None:
                tipo = TipoCotizacion(
                    id_tipo=None,
                    nombre=nombre_tipo,
                    descripcion=f"Cotización dólar {nombre_tipo} provista por DolarAPI",
                )
                tipo = self._repo_tipo.crear(tipo)

            # Registrar o actualizar la cotización en la base de datos
            cotizacion = CotizacionDolar(
                id_cotizacion=None,
                tipo_cotizacion=tipo,
                fecha=fecha_obj,
                compra=compra,
                venta=venta,
            )
            guardada = self._repo_cotizacion.crear(cotizacion)
            cotizaciones_registradas.append(guardada)

        return cotizaciones_registradas


# Alias solicitado por la consigna
ServicioCotizacionDolar = CotizacionService


class StockService:
    """Servicio de lógica de negocio para la administración de stock e inventario."""

    def __init__(self, repo_stock: RepositorioStock, repo_libro: RepositorioLibro) -> None:
        self._repo_stock = repo_stock
        self._repo_libro = repo_libro

    def registrar_stock_inicial(
        self,
        id_libro: int,
        cantidad: int = 0,
        ubicacion: str = "Depósito Central",
        id_stock: Optional[int] = None,
    ) -> Stock:
        libro = self._repo_libro.leer_por_id(id_libro)
        if not libro:
            raise ValueError(f"No existe el libro con ID {id_libro}.")
        if self._repo_stock.leer_por_libro(id_libro) is not None:
            raise ValueError(f"Ya existe un registro de stock para el libro '{libro.titulo}'.")
        nuevo_stock = Stock(id_stock=id_stock, libro=libro, cantidad=cantidad, ubicacion=ubicacion)
        return self._repo_stock.crear(nuevo_stock)

    def obtener_stock_por_libro(self, id_libro: int) -> Optional[Stock]:
        return self._repo_stock.leer_por_libro(id_libro)

    def agregar_unidades(self, id_libro: int, cantidad: int) -> Stock:
        if cantidad <= 0:
            raise ValueError("La cantidad a ingresar debe ser mayor que cero.")
        stock = self._repo_stock.leer_por_libro(id_libro)
        if not stock:
            raise ValueError(f"No existe stock registrado para el libro ID {id_libro}.")
        stock.cantidad += cantidad
        return self._repo_stock.actualizar(stock)

    def retirar_unidades(self, id_libro: int, cantidad: int) -> Stock:
        if cantidad <= 0:
            raise ValueError("La cantidad a retirar debe ser mayor que cero.")
        stock = self._repo_stock.leer_por_libro(id_libro)
        if not stock:
            raise ValueError(f"No existe stock registrado para el libro ID {id_libro}.")
        if stock.cantidad < cantidad:
            raise ValueError(
                f"Existencias insuficientes. Stock actual: {stock.cantidad}, solicitadas: {cantidad}."
            )
        stock.cantidad -= cantidad
        return self._repo_stock.actualizar(stock)

    def listar_todos(self) -> List[Stock]:
        return self._repo_stock.leer_todos()


class PrecioService:
    """Servicio de lógica de negocio para la cotización multimoneda y administración de precios."""

    def __init__(
        self,
        repo_precio: RepositorioPrecio,
        repo_libro: RepositorioLibro,
        repo_moneda: RepositorioMoneda,
        cotizacion_service: CotizacionService,
        tipo_cotizacion_service: TipoCotizacionService,
    ) -> None:
        self._repo_precio = repo_precio
        self._repo_libro = repo_libro
        self._repo_moneda = repo_moneda
        self._cotizacion_svc = cotizacion_service
        self._tipo_svc = tipo_cotizacion_service

    def fijar_precio(
        self,
        id_libro: int,
        id_moneda: int,
        valor: float,
        id_precio: Optional[int] = None,
    ) -> Precio:
        if valor < 0:
            raise ValueError("El valor del precio no puede ser negativo.")
        libro = self._repo_libro.leer_por_id(id_libro)
        if not libro:
            raise ValueError(f"No existe el libro con ID {id_libro}.")
        moneda = self._repo_moneda.leer_por_id(id_moneda)
        if not moneda:
            raise ValueError(f"No existe la moneda con ID {id_moneda}.")

        existente = self._repo_precio.leer_por_libro_y_moneda(id_libro, id_moneda)
        if existente:
            existente.valor = valor
            return self._repo_precio.actualizar(existente)

        nuevo_precio = Precio(id_precio=id_precio, libro=libro, moneda=moneda, valor=valor)
        return self._repo_precio.crear(nuevo_precio)

    def obtener_precio_por_libro_y_moneda(self, id_libro: int, id_moneda: int) -> Optional[Precio]:
        return self._repo_precio.leer_por_libro_y_moneda(id_libro, id_moneda)

    def listar_precios_por_libro(self, id_libro: int) -> List[Precio]:
        return self._repo_precio.leer_por_libro(id_libro)

    def listar_todos(self) -> List[Precio]:
        return self._repo_precio.leer_todos()

    def convertir_precio(
        self,
        monto: float,
        moneda_origen: str,
        moneda_destino: str,
        tipo_dolar: str = "Blue",
    ) -> float:
        """Convierte montos monetarios considerando cotizaciones vigentes del dólar."""
        origen = moneda_origen.strip().upper()
        destino = moneda_destino.strip().upper()

        if origen == destino:
            return round(monto, 2)

        tipo = self._tipo_svc.obtener_por_nombre(tipo_dolar)
        if not tipo:
            raise ValueError(f"Tipo de cotización '{tipo_dolar}' no encontrado.")

        cotizacion = self._cotizacion_svc.obtener_ultima_cotizacion(tipo.id)
        if not cotizacion:
            raise ValueError(f"No existen cotizaciones registradas para el tipo '{tipo_dolar}'.")

        tasa_dolar = cotizacion.venta
        if tasa_dolar <= 0:
            raise ValueError("La tasa de cotización debe ser mayor que cero.")

        if origen == "ARS" and destino == "USD":
            return round(monto / tasa_dolar, 2)
        elif origen == "USD" and destino == "ARS":
            return round(monto * tasa_dolar, 2)
        else:
            raise NotImplementedError(f"Conversión entre {origen} y {destino} no soportada.")

    def obtener_precio_estimado(
        self,
        id_libro: int,
        moneda_destino: str,
        tipo_dolar: str = "Blue",
    ) -> Optional[float]:
        """Retorna el precio de un libro en la divisa solicitada realizando conversiones si es necesario."""
        moneda_dest_obj = self._repo_moneda.buscar_por_codigo(moneda_destino)
        if not moneda_dest_obj:
            return None

        precio_directo = self._repo_precio.leer_por_libro_y_moneda(id_libro, moneda_dest_obj.id)
        if precio_directo:
            return precio_directo.valor

        # Si no tiene precio directo, intentar convertir desde ARS o USD
        moneda_ars = self._repo_moneda.buscar_por_codigo("ARS")
        if moneda_ars and moneda_destino.upper() == "USD":
            precio_ars = self._repo_precio.leer_por_libro_y_moneda(id_libro, moneda_ars.id)
            if precio_ars:
                try:
                    return self.convertir_precio(precio_ars.valor, "ARS", "USD", tipo_dolar)
                except (ValueError, NotImplementedError):
                    return None

        moneda_usd = self._repo_moneda.buscar_por_codigo("USD")
        if moneda_usd and moneda_destino.upper() == "ARS":
            precio_usd = self._repo_precio.leer_por_libro_y_moneda(id_libro, moneda_usd.id)
            if precio_usd:
                try:
                    return self.convertir_precio(precio_usd.valor, "USD", "ARS", tipo_dolar)
                except (ValueError, NotImplementedError):
                    return None

        return None


class LibroService:
    """Servicio de lógica de negocio para la gestión integral del catálogo de Libros."""

    def __init__(
        self,
        repo_libro: RepositorioLibro,
        repo_genero: RepositorioGenero,
        repo_editorial: RepositorioEditorial,
    ) -> None:
        self._repo_libro = repo_libro
        self._repo_genero = repo_genero
        self._repo_editorial = repo_editorial

    def dar_de_alta_libro(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        id_genero: int,
        id_editorial: int,
        anio_publicacion: Optional[int] = None,
        paginas: Optional[int] = None,
        id_libro: Optional[int] = None,
    ) -> Libro:
        if self._repo_libro.buscar_por_isbn(isbn) is not None:
            raise ValueError(f"Ya existe un libro registrado con el ISBN '{isbn}'.")

        genero = self._repo_genero.leer_por_id(id_genero)
        if not genero:
            raise ValueError(f"El género con ID {id_genero} no existe.")

        editorial = self._repo_editorial.leer_por_id(id_editorial)
        if not editorial:
            raise ValueError(f"La editorial con ID {id_editorial} no existe.")

        nuevo_libro = Libro(
            id_libro=id_libro,
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            genero=genero,
            editorial=editorial,
            anio_publicacion=anio_publicacion,
            paginas=paginas,
        )
        return self._repo_libro.crear(nuevo_libro)

    def obtener_por_id(self, id_libro: int) -> Optional[Libro]:
        return self._repo_libro.leer_por_id(id_libro)

    def obtener_por_isbn(self, isbn: str) -> Optional[Libro]:
        return self._repo_libro.buscar_por_isbn(isbn)

    def buscar_por_titulo(self, termino: str) -> List[Libro]:
        return self._repo_libro.buscar_por_titulo(termino)

    def buscar_por_autor(self, autor: str) -> List[Libro]:
        return self._repo_libro.buscar_por_autor(autor)

    def buscar_por_genero(self, id_genero: int) -> List[Libro]:
        return self._repo_libro.buscar_por_genero(id_genero)

    def buscar_por_editorial(self, id_editorial: int) -> List[Libro]:
        return self._repo_libro.buscar_por_editorial(id_editorial)

    def listar_todos(self) -> List[Libro]:
        return self._repo_libro.leer_todos()

    def actualizar_libro(
        self,
        id_libro: int,
        isbn: str,
        titulo: str,
        autor: str,
        id_genero: int,
        id_editorial: int,
        anio_publicacion: Optional[int] = None,
        paginas: Optional[int] = None,
    ) -> Libro:
        libro_existente = self._repo_libro.leer_por_id(id_libro)
        if not libro_existente:
            raise ValueError(f"No existe el libro con ID {id_libro}.")

        otro_isbn = self._repo_libro.buscar_por_isbn(isbn)
        if otro_isbn and otro_isbn.id != id_libro:
            raise ValueError(f"Ya existe otro libro registrado con el ISBN '{isbn}'.")

        genero = self._repo_genero.leer_por_id(id_genero)
        if not genero:
            raise ValueError(f"El género con ID {id_genero} no existe.")

        editorial = self._repo_editorial.leer_por_id(id_editorial)
        if not editorial:
            raise ValueError(f"La editorial con ID {id_editorial} no existe.")

        libro_existente.isbn = isbn
        libro_existente.titulo = titulo
        libro_existente.autor = autor
        libro_existente.genero = genero
        libro_existente.editorial = editorial
        libro_existente.anio_publicacion = anio_publicacion
        libro_existente.paginas = paginas

        return self._repo_libro.actualizar(libro_existente)

    def eliminar_libro(self, id_libro: int) -> bool:
        return self._repo_libro.eliminar(id_libro)


class ReporteService:
    """Servicio de agregación y reportería analítica del catálogo e inventario."""

    def __init__(
        self,
        libro_service: LibroService,
        stock_service: StockService,
        precio_service: PrecioService,
        genero_service: GeneroService,
        editorial_service: EditorialService,
        cotizacion_service: CotizacionService,
        tipo_cotizacion_service: TipoCotizacionService,
    ) -> None:
        self._libro_svc = libro_service
        self._stock_svc = stock_service
        self._precio_svc = precio_service
        self._genero_svc = genero_service
        self._editorial_svc = editorial_service
        self._cotizacion_svc = cotizacion_service
        self._tipo_svc = tipo_cotizacion_service

    def reporte_catalogo_completo(self, tipo_dolar: str = "Blue") -> List[Dict[str, Any]]:
        """Genera el catálogo consolidado de libros con existencias y precios en ARS y USD."""
        libros = self._libro_svc.listar_todos()
        resultado = []

        for libro in libros:
            genero = self._genero_svc.obtener_por_id(libro.id_genero)
            editorial = self._editorial_svc.obtener_por_id(libro.id_editorial)
            stock = self._stock_svc.obtener_stock_por_libro(libro.id)
            precio_ars = self._precio_svc.obtener_precio_estimado(libro.id, "ARS", tipo_dolar)
            precio_usd = self._precio_svc.obtener_precio_estimado(libro.id, "USD", tipo_dolar)

            resultado.append({
                "id": libro.id,
                "isbn": libro.isbn,
                "titulo": libro.titulo,
                "autor": libro.autor,
                "genero": genero.nombre if genero else "N/A",
                "editorial": editorial.nombre if editorial else "N/A",
                "stock": stock.cantidad if stock else 0,
                "precio_ars": precio_ars,
                "precio_usd": precio_usd,
            })
        return resultado

    def reporte_valorizacion_inventario(self, tipo_dolar: str = "Blue") -> Dict[str, Any]:
        """Calcula el valor total del inventario de libros en ARS y USD."""
        catalogo = self.reporte_catalogo_completo(tipo_dolar=tipo_dolar)
        total_unidades = sum(item["stock"] for item in catalogo)
        total_titulos = len(catalogo)
        valor_total_ars = sum((item["precio_ars"] or 0.0) * item["stock"] for item in catalogo)
        valor_total_usd = sum((item["precio_usd"] or 0.0) * item["stock"] for item in catalogo)

        return {
            "total_titulos": total_titulos,
            "total_ejemplares": total_unidades,
            "valor_total_ars": round(valor_total_ars, 2),
            "valor_total_usd": round(valor_total_usd, 2),
            "tipo_dolar_referencia": tipo_dolar,
        }

    def reporte_stock_critico(self, umbral: int = 5) -> List[Dict[str, Any]]:
        """Identifica libros con existencias inferiores o iguales al umbral establecido."""
        catalogo = self.reporte_catalogo_completo()
        return [item for item in catalogo if item["stock"] <= umbral]

    def reporte_distribucion_generos(self) -> Dict[str, int]:
        """Calcula la cantidad de libros disponibles por cada género."""
        distribucion: Dict[str, int] = {}
        for genero in self._genero_svc.listar_todos():
            distribucion[genero.nombre] = 0

        for libro in self._libro_svc.listar_todos():
            g = self._genero_svc.obtener_por_id(libro.id_genero)
            nombre_genero = g.nombre if g else "Sin Género"
            distribucion[nombre_genero] = distribucion.get(nombre_genero, 0) + 1

        return distribucion


class BookManagerService:
    """Coordinador central que implementa inyección de dependencias modular.

    Permite instanciar repositorios y servicios externamente o provee
    instancias predeterminadas conectadas a la base de datos relacional.
    """

    def __init__(
        self,
        repo_libro: Optional[RepositorioLibro] = None,
        repo_genero: Optional[RepositorioGenero] = None,
        repo_editorial: Optional[RepositorioEditorial] = None,
        repo_moneda: Optional[RepositorioMoneda] = None,
        repo_tipo_cotizacion: Optional[RepositorioTipoCotizacion] = None,
        repo_precio: Optional[RepositorioPrecio] = None,
        repo_stock: Optional[RepositorioStock] = None,
        repo_cotizacion: Optional[RepositorioCotizacionDolar] = None,
    ) -> None:
        # Inicialización de Repositorios con Inyección de Dependencias
        self.repo_libro = repo_libro or RepositorioLibro()
        self.repo_genero = repo_genero or RepositorioGenero()
        self.repo_editorial = repo_editorial or RepositorioEditorial()
        self.repo_moneda = repo_moneda or RepositorioMoneda()
        self.repo_tipo_cotizacion = repo_tipo_cotizacion or RepositorioTipoCotizacion()
        self.repo_precio = repo_precio or RepositorioPrecio()
        self.repo_stock = repo_stock or RepositorioStock()
        self.repo_cotizacion = repo_cotizacion or RepositorioCotizacionDolar()

        # Inicialización de Servicios
        self.genero_service = GeneroService(self.repo_genero)
        self.editorial_service = EditorialService(self.repo_editorial)
        self.moneda_service = MonedaService(self.repo_moneda)
        self.tipo_cotizacion_service = TipoCotizacionService(self.repo_tipo_cotizacion)
        self.cotizacion_service = CotizacionService(self.repo_cotizacion, self.repo_tipo_cotizacion)
        self.libro_service = LibroService(self.repo_libro, self.repo_genero, self.repo_editorial)
        self.stock_service = StockService(self.repo_stock, self.repo_libro)
        self.precio_service = PrecioService(
            self.repo_precio,
            self.repo_libro,
            self.repo_moneda,
            self.cotizacion_service,
            self.tipo_cotizacion_service,
        )
        self.reporte_service = ReporteService(
            self.libro_service,
            self.stock_service,
            self.precio_service,
            self.genero_service,
            self.editorial_service,
            self.cotizacion_service,
            self.tipo_cotizacion_service,
        )
