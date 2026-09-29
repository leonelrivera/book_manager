"""Capa de servicios y lógica de negocio para el sistema Book Manager.

Contiene los servicios encargados de implementar las reglas de negocio,
conversión de divisas, gestión de stock, orquestación de operaciones CRUD
y generación de reportes analíticos del catálogo.
"""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple, Union

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
        if cantidad < 0:
            raise ValueError("La cantidad de stock no puede ser negativa.")

        stock_existente = self._repo_stock.leer_por_libro(id_libro)
        if stock_existente:
            stock_existente.cantidad = cantidad
            stock_existente.ubicacion = ubicacion
            return self._repo_stock.actualizar(stock_existente)

        nuevo_stock = Stock(id_stock=id_stock, libro=libro, cantidad=cantidad, ubicacion=ubicacion)
        return self._repo_stock.crear(nuevo_stock)

    def obtener_stock_por_libro(self, id_libro: int) -> Optional[Stock]:
        return self._repo_stock.leer_por_libro(id_libro)

    def listar_todo(self) -> List[Stock]:
        return self._repo_stock.leer_todos()

    def incrementar_stock(self, id_libro: int, cantidad_a_sumar: int) -> Stock:
        if cantidad_a_sumar <= 0:
            raise ValueError("La cantidad a sumar debe ser mayor a 0.")
        stock = self._repo_stock.leer_por_libro(id_libro)
        if not stock:
            return self.registrar_stock_inicial(id_libro, cantidad=cantidad_a_sumar)
        stock.cantidad += cantidad_a_sumar
        return self._repo_stock.actualizar(stock)

    def decrementar_stock(self, id_libro: int, cantidad_a_restar: int) -> Stock:
        if cantidad_a_restar <= 0:
            raise ValueError("La cantidad a restar debe ser mayor a 0.")
        stock = self._repo_stock.leer_por_libro(id_libro)
        if not stock:
            raise ValueError(f"No existe registro de stock para el libro ID {id_libro}.")
        if stock.cantidad < cantidad_a_restar:
            raise ValueError(
                f"Stock insuficiente. Disponible: {stock.cantidad}, Solicitado: {cantidad_a_restar}."
            )
        stock.cantidad -= cantidad_a_restar
        return self._repo_stock.actualizar(stock)

    def eliminar_stock(self, id_libro: int) -> bool:
        return self._repo_stock.eliminar(id_libro)


class PrecioService:
    """Servicio de lógica de negocio para la gestión de precios y conversiones monetarias."""

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
        self._cotizacion_service = cotizacion_service
        self._tipo_service = tipo_cotizacion_service

    def fijar_precio(
        self,
        id_libro: int,
        id_moneda: int,
        valor: float,
        id_precio: Optional[int] = None,
    ) -> Precio:
        libro = self._repo_libro.leer_por_id(id_libro)
        if not libro:
            raise ValueError(f"No existe el libro con ID {id_libro}.")
        moneda = self._repo_moneda.leer_por_id(id_moneda)
        if not moneda:
            raise ValueError(f"No existe la moneda con ID {id_moneda}.")
        if valor < 0:
            raise ValueError("El valor del precio no puede ser negativo.")

        precio_existente = self._repo_precio.leer_por_libro_y_moneda(id_libro, id_moneda)
        if precio_existente:
            precio_existente.valor = valor
            return self._repo_precio.actualizar(precio_existente)

        nuevo_precio = Precio(id_precio=id_precio, libro=libro, moneda=moneda, valor=valor)
        return self._repo_precio.crear(nuevo_precio)

    def obtener_precio(self, id_libro: int, id_moneda: int) -> Optional[Precio]:
        return self._repo_precio.leer_por_libro_y_moneda(id_libro, id_moneda)

    def obtener_todos_por_libro(self, id_libro: int) -> List[Precio]:
        return self._repo_precio.leer_por_libro(id_libro)

    def listar_todos(self) -> List[Precio]:
        return self._repo_precio.leer_todos()

    def eliminar_precio(self, id_libro: int, id_moneda: int) -> bool:
        return self._repo_precio.eliminar_por_libro_y_moneda(id_libro, id_moneda)

    def convertir_monto(
        self,
        monto_origen: float,
        codigo_moneda_origen: str,
        codigo_moneda_destino: str,
        nombre_tipo_cotizacion: str = "Blue",
        usar_venta: bool = True,
    ) -> float:
        """Convierte un monto entre ARS y USD utilizando la cotización del dólar indicada."""
        cod_origen = codigo_moneda_origen.strip().upper()
        cod_destino = codigo_moneda_destino.strip().upper()

        if cod_origen == cod_destino:
            return round(monto_origen, 2)

        tipo = self._tipo_service.obtener_por_nombre(nombre_tipo_cotizacion)
        if not tipo or tipo.id is None:
            raise ValueError(f"Tipo de cotización '{nombre_tipo_cotizacion}' no disponible.")

        cotizacion = self._cotizacion_service.obtener_ultima_cotizacion(tipo.id)
        if not cotizacion:
            raise ValueError(f"No hay registros de cotización para '{nombre_tipo_cotizacion}'.")

        tasa = cotizacion.venta if usar_venta else cotizacion.compra
        if tasa <= 0:
            raise ValueError("La tasa de cotización debe ser mayor a 0.")

        match (cod_origen, cod_destino):
            case ("USD", "ARS"):
                return round(monto_origen * tasa, 2)
            case ("ARS", "USD"):
                return round(monto_origen / tasa, 2)
            case _:
                raise NotImplementedError(f"Conversión no soportada entre {cod_origen} y {cod_destino}.")

    def obtener_precio_estimado(
        self,
        id_libro: int,
        codigo_moneda_destino: str,
        nombre_tipo_cotizacion: str = "Blue",
    ) -> Optional[float]:
        """Calcula el precio de un libro en la moneda solicitada convirtiendo si es necesario."""
        moneda_dest = self._repo_moneda.buscar_por_codigo(codigo_moneda_destino)
        if not moneda_dest or moneda_dest.id is None:
            return None

        # Si ya tiene precio directo fijado en esa moneda
        precio_directo = self._repo_precio.leer_por_libro_y_moneda(id_libro, moneda_dest.id)
        if precio_directo:
            return precio_directo.valor

        # Si no tiene precio directo, buscar en otra moneda y convertir
        precios_libro = self._repo_precio.leer_por_libro(id_libro)
        for p in precios_libro:
            moneda_origen = self._repo_moneda.leer_por_id(p.id_moneda)
            if moneda_origen:
                try:
                    return self.convertir_monto(
                        p.valor,
                        moneda_origen.codigo,
                        codigo_moneda_destino,
                        nombre_tipo_cotizacion,
                    )
                except Exception:
                    continue
        return None


class LibroService:
    """Servicio de lógica de negocio para la administración del catálogo de libros."""

    def __init__(
        self,
        repo_libro: RepositorioLibro,
        repo_genero: RepositorioGenero,
        repo_editorial: RepositorioEditorial,
    ) -> None:
        self._repo_libro = repo_libro
        self._repo_genero = repo_genero
        self._repo_editorial = repo_editorial

    def crear_libro(
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
        genero_obj = self._repo_genero.leer_por_id(id_genero)
        if not genero_obj:
            raise ValueError(f"No existe el género literario con ID {id_genero}.")
        editorial_obj = self._repo_editorial.leer_por_id(id_editorial)
        if not editorial_obj:
            raise ValueError(f"No existe la editorial con ID {id_editorial}.")

        nuevo_libro = Libro(
            id_libro=id_libro,
            isbn=isbn,
            titulo=titulo,
            autor=autor,
            genero=genero_obj,
            editorial=editorial_obj,
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
            raise ValueError(f"El ISBN '{isbn}' ya pertenece a otro libro.")

        genero_obj = self._repo_genero.leer_por_id(id_genero)
        if not genero_obj:
            raise ValueError(f"No existe el género con ID {id_genero}.")
        editorial_obj = self._repo_editorial.leer_por_id(id_editorial)
        if not editorial_obj:
            raise ValueError(f"No existe la editorial con ID {id_editorial}.")

        libro_existente.isbn = isbn
        libro_existente.titulo = titulo
        libro_existente.autor = autor
        libro_existente.genero = genero_obj
        libro_existente.editorial = editorial_obj
        libro_existente.anio_publicacion = anio_publicacion
        libro_existente.paginas = paginas

        return self._repo_libro.actualizar(libro_existente)

    def eliminar_libro(self, id_libro: int) -> bool:
        return self._repo_libro.eliminar(id_libro)


class ReporteService:
    """Servicio para la generación de reportes e indicadores del sistema."""

    def __init__(
        self,
        libro_service: LibroService,
        stock_service: StockService,
        precio_service: PrecioService,
        genero_service: GeneroService,
        editorial_service: EditorialService,
        cotizacion_service: CotizacionService,
        tipo_service: TipoCotizacionService,
    ) -> None:
        self._libro_svc = libro_service
        self._stock_svc = stock_service
        self._precio_svc = precio_service
        self._genero_svc = genero_service
        self._editorial_svc = editorial_service
        self._cotizacion_svc = cotizacion_service
        self._tipo_svc = tipo_service

    def reporte_catalogo_completo(self, tipo_dolar: str = "Blue") -> List[Dict[str, Any]]:
        """Genera un listado detallado de libros con género, editorial, precios y stock."""
        resultado = []
        for libro in self._libro_svc.listar_todos():
            if libro.id is None:
                continue
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
    """Coordinador central que agrupa e inicializa todos los servicios del sistema."""

    def __init__(self) -> None:
        # Inicialización de Repositorios
        self.repo_libro = RepositorioLibro()
        self.repo_genero = RepositorioGenero()
        self.repo_editorial = RepositorioEditorial()
        self.repo_moneda = RepositorioMoneda()
        self.repo_tipo_cotizacion = RepositorioTipoCotizacion()
        self.repo_precio = RepositorioPrecio()
        self.repo_stock = RepositorioStock()
        self.repo_cotizacion = RepositorioCotizacionDolar()

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
