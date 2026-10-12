"""Capa de persistencia y repositorios para el sistema Book Manager.

Implementa los repositorios concretos utilizando SQLAlchemy 2.0 y modelos ORM
para interactuar con la base de datos relacional (PostgreSQL / Supabase / SQLite),
manteniendo la interfaz orientada a objetos (IRepositorio) y asegurando integridad
referencial en operaciones CRUD.
"""

import abc
from datetime import date, datetime
from typing import Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from book_manager.database.connection import ConexionDB, transaccion_db
from book_manager.entities.entities import (
    CotizacionDolar,
    Editorial,
    EntidadBase,
    Genero,
    Libro,
    Moneda,
    Precio,
    Stock,
    TipoCotizacion,
)
from book_manager.models.models import (
    Base,
    CotizacionDolarModel,
    EditorialModel,
    GeneroModel,
    LibroModel,
    MonedaModel,
    PrecioModel,
    StockModel,
    TipoCotizacionModel,
)

T = TypeVar("T", bound=EntidadBase)
M = TypeVar("M", bound=Base)


class IRepositorio(abc.ABC, Generic[T]):
    """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

    @abc.abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una nueva entidad en la base de datos."""
        pass

    @abc.abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        """Lee una entidad por su ID."""
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[T]:
        """Lee todas las entidades de la tabla."""
        pass

    @abc.abstractmethod
    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente."""
        pass

    @abc.abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad por su ID respetando restricciones de integridad."""
        pass


class IRepositorioStock(abc.ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        pass


class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para repositorios del tipo CotizacionDolar."""

    @abc.abstractmethod
    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: Union[date, str]) -> Optional[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        pass

    @abc.abstractmethod
    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        pass

    @abc.abstractmethod
    def eliminar(self, tipo_id: int, fecha: Union[date, str]) -> bool:
        pass


class RepositorioBase(IRepositorio[T], Generic[T, M]):
    """Implementación base de repositorio conectada a SQLAlchemy con conversión entidad <-> ORM."""

    def __init__(
        self,
        modelo_cls: Type[M],
        conexion: Optional[ConexionDB] = None,
        archivo_csv: Optional[str] = None,
    ) -> None:
        self._modelo_cls = modelo_cls
        self._conexion = conexion or ConexionDB.get_instancia()
        self._archivo_csv = archivo_csv

    def set_archivo_csv(self, ruta_csv: str) -> None:
        """Mantiene compatibilidad con la interfaz previa de CSV sin alterar la BD."""
        self._archivo_csv = ruta_csv

    def guardar_en_csv(self) -> None:
        """Compatibilidad con versiones anteriores."""
        pass

    def _obtener_sesion(self) -> Session:
        return self._conexion.crear_sesion()

    def _a_entidad(self, modelo: M) -> T:
        """Convierte una fila del modelo ORM a una instancia de entidad de dominio."""
        raise NotImplementedError

    def _a_modelo(self, entidad: T) -> M:
        """Convierte una entidad de dominio a un objeto ORM mapeado."""
        raise NotImplementedError

    def crear(self, entidad: T) -> T:
        with transaccion_db() as session:
            modelo = self._a_modelo(entidad)
            session.add(modelo)
            session.flush()
            entidad.id = modelo.id
            return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        with transaccion_db() as session:
            modelo = session.get(self._modelo_cls, id)
            if modelo is None:
                return None
            return self._a_entidad(modelo)

    def leer_todos(self) -> List[T]:
        with transaccion_db() as session:
            stmt = select(self._modelo_cls).order_by(self._modelo_cls.id)
            modelos = session.scalars(stmt).all()
            return [self._a_entidad(m) for m in modelos]

    def actualizar(self, entidad: T) -> T:
        if entidad.id is None:
            raise ValueError("No se puede actualizar una entidad sin ID.")
        with transaccion_db() as session:
            modelo = session.get(self._modelo_cls, entidad.id)
            if modelo is None:
                raise ValueError(f"No se encuentra la entidad con ID {entidad.id} para actualizar.")
            nuevo_modelo = self._a_modelo(entidad)
            for attr in dir(nuevo_modelo):
                if not attr.startswith("_") and attr not in ("metadata", "registry"):
                    val = getattr(nuevo_modelo, attr)
                    if hasattr(modelo, attr) and not callable(val):
                        setattr(modelo, attr, val)
            session.flush()
            return entidad

    def eliminar(self, id: int) -> bool:
        with transaccion_db() as session:
            modelo = session.get(self._modelo_cls, id)
            if modelo is not None:
                session.delete(modelo)
                return True
            return False

    def vaciar(self) -> None:
        """Limpia todos los registros de la tabla en la base de datos."""
        with transaccion_db() as session:
            session.execute(delete(self._modelo_cls))


class RepositorioGenero(RepositorioBase[Genero, GeneroModel]):
    """Repositorio para la entidad Genero conectado a la tabla 'generos'."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(GeneroModel, conexion, archivo_csv)

    def _a_entidad(self, modelo: GeneroModel) -> Genero:
        return Genero(id_genero=modelo.id, nombre=modelo.nombre, descripcion=modelo.descripcion or "")

    def _a_modelo(self, entidad: Genero) -> GeneroModel:
        return GeneroModel(id=entidad.id, nombre=entidad.nombre, descripcion=entidad.descripcion)

    def buscar_por_nombre(self, nombre: str) -> Optional[Genero]:
        with transaccion_db() as session:
            stmt = select(GeneroModel).where(GeneroModel.nombre.ilike(nombre.strip()))
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def tiene_libros_asociados(self, id_genero: int) -> bool:
        """Verifica si existen libros vinculados al género antes de eliminar."""
        with transaccion_db() as session:
            stmt = select(LibroModel.id).where(LibroModel.id_genero == id_genero).limit(1)
            return session.scalars(stmt).first() is not None

    def eliminar(self, id: int) -> bool:
        if self.tiene_libros_asociados(id):
            raise ValueError(f"No se puede eliminar el género con ID {id} porque tiene libros asociados.")
        return super().eliminar(id)


class RepositorioEditorial(RepositorioBase[Editorial, EditorialModel]):
    """Repositorio para la entidad Editorial conectado a la tabla 'editoriales'."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(EditorialModel, conexion, archivo_csv)

    def _a_entidad(self, modelo: EditorialModel) -> Editorial:
        return Editorial(
            id_editorial=modelo.id,
            nombre=modelo.nombre,
            pais=modelo.pais or "Argentina",
            contacto=modelo.contacto or "",
        )

    def _a_modelo(self, entidad: Editorial) -> EditorialModel:
        return EditorialModel(
            id=entidad.id,
            nombre=entidad.nombre,
            pais=entidad.pais,
            contacto=entidad.contacto,
        )

    def buscar_por_nombre(self, nombre: str) -> Optional[Editorial]:
        with transaccion_db() as session:
            stmt = select(EditorialModel).where(EditorialModel.nombre.ilike(nombre.strip()))
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def tiene_libros_asociados(self, id_editorial: int) -> bool:
        """Verifica si existen libros vinculados a la editorial antes de eliminar."""
        with transaccion_db() as session:
            stmt = select(LibroModel.id).where(LibroModel.id_editorial == id_editorial).limit(1)
            return session.scalars(stmt).first() is not None

    def eliminar(self, id: int) -> bool:
        if self.tiene_libros_asociados(id):
            raise ValueError(f"No se puede eliminar la editorial con ID {id} porque tiene libros asociados.")
        return super().eliminar(id)


class RepositorioMoneda(RepositorioBase[Moneda, MonedaModel]):
    """Repositorio para la entidad Moneda conectado a la tabla 'monedas'."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(MonedaModel, conexion, archivo_csv)

    def _a_entidad(self, modelo: MonedaModel) -> Moneda:
        return Moneda(
            id_moneda=modelo.id,
            codigo=modelo.codigo,
            nombre=modelo.nombre,
            simbolo=modelo.simbolo or "$",
        )

    def _a_modelo(self, entidad: Moneda) -> MonedaModel:
        return MonedaModel(
            id=entidad.id,
            codigo=entidad.codigo,
            nombre=entidad.nombre,
            simbolo=entidad.simbolo,
        )

    def buscar_por_codigo(self, codigo: str) -> Optional[Moneda]:
        with transaccion_db() as session:
            stmt = select(MonedaModel).where(MonedaModel.codigo.ilike(codigo.strip()))
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def tiene_precios_asociados(self, id_moneda: int) -> bool:
        """Verifica si existen precios expresados en esta moneda antes de eliminar."""
        with transaccion_db() as session:
            stmt = select(PrecioModel.id).where(PrecioModel.id_moneda == id_moneda).limit(1)
            return session.scalars(stmt).first() is not None

    def eliminar(self, id: int) -> bool:
        if self.tiene_precios_asociados(id):
            raise ValueError(f"No se puede eliminar la moneda con ID {id} porque existen precios asociados.")
        return super().eliminar(id)


class RepositorioTipoCotizacion(RepositorioBase[TipoCotizacion, TipoCotizacionModel]):
    """Repositorio para la entidad TipoCotizacion conectado a la tabla 'tipos_cotizacion'."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(TipoCotizacionModel, conexion, archivo_csv)

    def _a_entidad(self, modelo: TipoCotizacionModel) -> TipoCotizacion:
        return TipoCotizacion(id_tipo=modelo.id, nombre=modelo.nombre, descripcion=modelo.descripcion or "")

    def _a_modelo(self, entidad: TipoCotizacion) -> TipoCotizacionModel:
        return TipoCotizacionModel(id=entidad.id, nombre=entidad.nombre, descripcion=entidad.descripcion)

    def buscar_por_nombre(self, nombre: str) -> Optional[TipoCotizacion]:
        with transaccion_db() as session:
            stmt = select(TipoCotizacionModel).where(TipoCotizacionModel.nombre.ilike(nombre.strip()))
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def tiene_cotizaciones_asociadas(self, id_tipo: int) -> bool:
        """Verifica si existen cotizaciones registradas para este tipo."""
        with transaccion_db() as session:
            stmt = select(CotizacionDolarModel.id).where(CotizacionDolarModel.id_tipo == id_tipo).limit(1)
            return session.scalars(stmt).first() is not None

    def eliminar(self, id: int) -> bool:
        if self.tiene_cotizaciones_asociadas(id):
            raise ValueError(f"No se puede eliminar el tipo de cotización con ID {id} porque tiene cotizaciones asociadas.")
        return super().eliminar(id)


class RepositorioLibro(RepositorioBase[Libro, LibroModel]):
    """Repositorio para la entidad Libro con relaciones cargadas y búsquedas especializadas."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(LibroModel, conexion, archivo_csv)

    def _a_entidad(self, modelo: LibroModel) -> Libro:
        genero_entidad = Genero(
            id_genero=modelo.genero.id,
            nombre=modelo.genero.nombre,
            descripcion=modelo.genero.descripcion or "",
        ) if modelo.genero else modelo.id_genero

        editorial_entidad = Editorial(
            id_editorial=modelo.editorial.id,
            nombre=modelo.editorial.nombre,
            pais=modelo.editorial.pais or "Argentina",
            contacto=modelo.editorial.contacto or "",
        ) if modelo.editorial else modelo.id_editorial

        return Libro(
            id_libro=modelo.id,
            isbn=modelo.isbn,
            titulo=modelo.titulo,
            autor=modelo.autor,
            genero=genero_entidad,
            editorial=editorial_entidad,
            anio_publicacion=modelo.anio_publicacion,
            paginas=modelo.paginas,
        )

    def _a_modelo(self, entidad: Libro) -> LibroModel:
        return LibroModel(
            id=entidad.id,
            isbn=entidad.isbn,
            titulo=entidad.titulo,
            autor=entidad.autor,
            anio_publicacion=entidad.anio_publicacion,
            paginas=entidad.paginas,
            id_genero=entidad.id_genero,
            id_editorial=entidad.id_editorial,
        )

    def buscar_por_isbn(self, isbn: str) -> Optional[Libro]:
        with transaccion_db() as session:
            stmt = select(LibroModel).where(LibroModel.isbn.ilike(isbn.strip()))
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def buscar_por_titulo(self, termino: str) -> List[Libro]:
        with transaccion_db() as session:
            stmt = select(LibroModel).where(LibroModel.titulo.ilike(f"%{termino.strip()}%"))
            modelos = session.scalars(stmt).all()
            return [self._a_entidad(m) for m in modelos]

    def buscar_por_autor(self, autor: str) -> List[Libro]:
        with transaccion_db() as session:
            stmt = select(LibroModel).where(LibroModel.autor.ilike(f"%{autor.strip()}%"))
            modelos = session.scalars(stmt).all()
            return [self._a_entidad(m) for m in modelos]

    def buscar_por_genero(self, id_genero: int) -> List[Libro]:
        with transaccion_db() as session:
            stmt = select(LibroModel).where(LibroModel.id_genero == id_genero)
            modelos = session.scalars(stmt).all()
            return [self._a_entidad(m) for m in modelos]

    def buscar_por_editorial(self, id_editorial: int) -> List[Libro]:
        with transaccion_db() as session:
            stmt = select(LibroModel).where(LibroModel.id_editorial == id_editorial)
            modelos = session.scalars(stmt).all()
            return [self._a_entidad(m) for m in modelos]


class RepositorioPrecio(RepositorioBase[Precio, PrecioModel]):
    """Repositorio para la entidad Precio conectado a la tabla 'precios'."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(PrecioModel, conexion, archivo_csv)

    def _a_entidad(self, modelo: PrecioModel) -> Precio:
        return Precio(
            id_precio=modelo.id,
            id_libro=modelo.id_libro,
            id_moneda=modelo.id_moneda,
            valor=modelo.valor,
        )

    def _a_modelo(self, entidad: Precio) -> PrecioModel:
        return PrecioModel(
            id=entidad.id,
            id_libro=entidad.id_libro,
            id_moneda=entidad.id_moneda,
            valor=entidad.valor,
        )

    def leer_por_libro_y_moneda(self, id_libro: int, id_moneda: int) -> Optional[Precio]:
        with transaccion_db() as session:
            stmt = select(PrecioModel).where(
                PrecioModel.id_libro == id_libro,
                PrecioModel.id_moneda == id_moneda,
            )
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def leer_por_libro(self, id_libro: int) -> List[Precio]:
        with transaccion_db() as session:
            stmt = select(PrecioModel).where(PrecioModel.id_libro == id_libro)
            modelos = session.scalars(stmt).all()
            return [self._a_entidad(m) for m in modelos]

    def eliminar_por_libro_y_moneda(self, id_libro: int, id_moneda: int) -> bool:
        with transaccion_db() as session:
            stmt = select(PrecioModel).where(
                PrecioModel.id_libro == id_libro,
                PrecioModel.id_moneda == id_moneda,
            )
            modelo = session.scalars(stmt).first()
            if modelo is not None:
                session.delete(modelo)
                return True
            return False


class RepositorioStock(RepositorioBase[Stock, StockModel], IRepositorioStock):
    """Repositorio para la entidad Stock conectado a la tabla 'stock'."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(StockModel, conexion, archivo_csv)

    def _a_entidad(self, modelo: StockModel) -> Stock:
        return Stock(
            id_stock=modelo.id,
            id_libro=modelo.id_libro,
            cantidad=modelo.cantidad,
            ubicacion=modelo.ubicacion,
        )

    def _a_modelo(self, entidad: Stock) -> StockModel:
        return StockModel(
            id=entidad.id,
            id_libro=entidad.id_libro,
            cantidad=entidad.cantidad,
            ubicacion=entidad.ubicacion,
        )

    def crear(self, stock: Stock) -> Stock:
        if self.leer_por_libro(stock.id_libro) is not None:
            raise ValueError(f"Ya existe un registro de stock para el libro con ID {stock.id_libro}.")
        return super().crear(stock)

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        with transaccion_db() as session:
            stmt = select(StockModel).where(StockModel.id_libro == libro_id)
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def actualizar(self, stock: Stock) -> Stock:
        existente = self.leer_por_libro(stock.id_libro)
        if existente is None:
            raise ValueError(f"No se encuentra el stock para el libro ID {stock.id_libro} para actualizar.")
        stock.id = existente.id
        return super().actualizar(stock)

    def eliminar(self, libro_id: int) -> bool:
        with transaccion_db() as session:
            stmt = select(StockModel).where(StockModel.id_libro == libro_id)
            modelo = session.scalars(stmt).first()
            if modelo is not None:
                session.delete(modelo)
                return True
            return False


class RepositorioCotizacionDolar(RepositorioBase[CotizacionDolar, CotizacionDolarModel], IRepositorioCotizacionDolar):
    """Repositorio para la entidad CotizacionDolar conectado a la tabla 'cotizaciones'."""

    def __init__(self, conexion: Optional[ConexionDB] = None, archivo_csv: Optional[str] = None) -> None:
        super().__init__(CotizacionDolarModel, conexion, archivo_csv)

    def _normalizar_fecha(self, fecha: Union[date, str]) -> date:
        if isinstance(fecha, str):
            return datetime.strptime(fecha.strip(), "%Y-%m-%d").date()
        return fecha

    def _a_entidad(self, modelo: CotizacionDolarModel) -> CotizacionDolar:
        return CotizacionDolar(
            id_cotizacion=modelo.id,
            id_tipo=modelo.id_tipo,
            fecha=modelo.fecha,
            compra=modelo.compra,
            venta=modelo.venta,
        )

    def _a_modelo(self, entidad: CotizacionDolar) -> CotizacionDolarModel:
        return CotizacionDolarModel(
            id=entidad.id,
            id_tipo=entidad.id_tipo,
            fecha=self._normalizar_fecha(entidad.fecha),
            compra=entidad.compra,
            venta=entidad.venta,
        )

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        fecha_norm = self._normalizar_fecha(cotizacion.fecha)
        existente = self.leer_por_tipo_y_fecha(cotizacion.id_tipo, fecha_norm)
        if existente is not None:
            # Si ya existe cotización para esa fecha y tipo, actualizamos los valores
            cotizacion.id = existente.id
            return self.actualizar(cotizacion)
        return super().crear(cotizacion)

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: Union[date, str]) -> Optional[CotizacionDolar]:
        fecha_norm = self._normalizar_fecha(fecha)
        with transaccion_db() as session:
            stmt = select(CotizacionDolarModel).where(
                CotizacionDolarModel.id_tipo == tipo_id,
                CotizacionDolarModel.fecha == fecha_norm,
            )
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        with transaccion_db() as session:
            stmt = select(CotizacionDolarModel).where(
                CotizacionDolarModel.id_tipo == tipo_id
            ).order_by(CotizacionDolarModel.fecha)
            modelos = session.scalars(stmt).all()
            return [self._a_entidad(m) for m in modelos]

    def leer_ultima_cotizacion(self, tipo_id: int) -> Optional[CotizacionDolar]:
        with transaccion_db() as session:
            stmt = select(CotizacionDolarModel).where(
                CotizacionDolarModel.id_tipo == tipo_id
            ).order_by(CotizacionDolarModel.fecha.desc()).limit(1)
            modelo = session.scalars(stmt).first()
            return self._a_entidad(modelo) if modelo else None

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        fecha_norm = self._normalizar_fecha(cotizacion.fecha)
        existente = self.leer_por_tipo_y_fecha(cotizacion.id_tipo, fecha_norm)
        if existente is None:
            raise ValueError(
                f"No se encuentra la cotización para el tipo {cotizacion.id_tipo} en fecha {fecha_norm} para actualizar."
            )
        cotizacion.id = existente.id
        return super().actualizar(cotizacion)

    def eliminar(self, tipo_id: int, fecha: Union[date, str]) -> bool:
        fecha_norm = self._normalizar_fecha(fecha)
        with transaccion_db() as session:
            stmt = select(CotizacionDolarModel).where(
                CotizacionDolarModel.id_tipo == tipo_id,
                CotizacionDolarModel.fecha == fecha_norm,
            )
            modelo = session.scalars(stmt).first()
            if modelo is not None:
                session.delete(modelo)
                return True
            return False
