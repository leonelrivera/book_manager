"""Capa de persistencia y repositorios para el sistema Book Manager.

Define las interfaces abstractas (IRepositorio, IRepositorioStock, IRepositorioCotizacionDolar)
y las implementaciones concretas para la gestión CRUD con persistencia activa en archivos CSV.
"""

import abc
import csv
from datetime import date, datetime
import os
from typing import Dict, Generic, List, Optional, Tuple, TypeVar, Union

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

T = TypeVar("T", bound=EntidadBase)


class IRepositorio(abc.ABC, Generic[T]):
    """Interfaz para repositorios que manejan entidades con operaciones CRUD básicas."""

    @abc.abstractmethod
    def crear(self, entidad: T) -> T:
        """Crea una nueva entidad en el repositorio.

        Args:
            entidad (T): La entidad a crear.

        Returns:
            T: La entidad creada.

        Raises:
            ValueError: Si ya existe una entidad con el mismo ID.
        """
        pass

    @abc.abstractmethod
    def leer_por_id(self, id: int) -> Optional[T]:
        """Lee una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a leer.

        Returns:
            Optional[T]: La entidad si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_todos(self) -> List[T]:
        """Lee todas las entidades del repositorio.

        Returns:
            List[T]: Una lista de todas las entidades.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, entidad: T) -> T:
        """Actualiza una entidad existente en el repositorio.

        Args:
            entidad (T): La entidad a actualizar (debe tener un ID existente).

        Returns:
            T: La entidad actualizada.

        Raises:
            ValueError: Si no se encuentra la entidad para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una entidad del repositorio por su ID.

        Args:
            id (int): El ID de la entidad a eliminar.

        Returns:
            bool: True si la entidad fue eliminada, False si no se encontró.
        """
        pass


class IRepositorioStock(abc.ABC):
    """Interfaz para repositorios del tipo Stock."""

    @abc.abstractmethod
    def crear(self, stock: Stock) -> Stock:
        """Crea un nuevo registro de stock.

        Args:
            stock (Stock): El objeto Stock a crear.

        Returns:
            Stock: El objeto Stock creado.

        Raises:
            ValueError: Si ya existe un registro de stock para el mismo libro.
        """
        pass

    @abc.abstractmethod
    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        """Lee un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock.

        Returns:
            Optional[Stock]: El objeto Stock si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, stock: Stock) -> Stock:
        """Actualiza un registro de stock existente.

        Args:
            stock (Stock): El objeto Stock a actualizar (debe tener un libro_id existente).

        Returns:
            Stock: El objeto Stock actualizado.

        Raises:
            ValueError: Si no se encuentra el stock para actualizar.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        """Elimina un registro de stock por ID de libro.

        Args:
            libro_id (int): El ID del libro asociado al stock a eliminar.

        Returns:
            bool: True si el stock fue eliminado, False si no se encontró.
        """
        pass


class IRepositorioCotizacionDolar(abc.ABC):
    """Interfaz para repositorios del tipo RepositorioCotizacionDolar."""

    @abc.abstractmethod
    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Crea una nueva cotización de dólar.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a crear.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar creado.

        Raises:
            ValueError: Si ya existe una cotización para el mismo tipo y fecha.
        """
        pass

    @abc.abstractmethod
    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: Union[date, str]) -> Optional[CotizacionDolar]:
        """Lee una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización (e.g., 'Oficial', 'Blue').
            fecha (date | str): La fecha de la cotización.

        Returns:
            Optional[CotizacionDolar]: La cotización si se encuentra, None en caso contrario.
        """
        pass

    @abc.abstractmethod
    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        """Lee el histórico de cotizaciones para un tipo específico.

        Args:
            tipo_id (int): El ID del tipo de cotización.

        Returns:
            List[CotizacionDolar]: Una lista de cotizaciones históricas para el tipo dado.
        """
        pass

    @abc.abstractmethod
    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        """Actualiza una cotización de dólar existente.

        Args:
            cotizacion (CotizacionDolar): El objeto CotizacionDolar a actualizar.

        Returns:
            CotizacionDolar: El objeto CotizacionDolar actualizado.
        """
        pass

    @abc.abstractmethod
    def eliminar(self, tipo_id: int, fecha: Union[date, str]) -> bool:
        """Elimina una cotización de dólar por tipo y fecha.

        Args:
            tipo_id (int): El ID del tipo de cotización.
            fecha (date | str): La fecha de la cotización a eliminar.

        Returns:
            bool: True si la cotización fue eliminada, False si no se encontró.
        """
        pass


class RepositorioBase(IRepositorio[T]):
    """Implementación genérica con soporte para almacenamiento en memoria y persistencia activa en CSV."""

    def __init__(self, archivo_csv: Optional[str] = None) -> None:
        self._datos: Dict[int, T] = {}
        self._siguiente_id: int = 1
        self._archivo_csv: Optional[str] = archivo_csv

    def set_archivo_csv(self, ruta_csv: str) -> None:
        """Configura el archivo CSV de destino para la persistencia automática."""
        self._archivo_csv = ruta_csv

    def guardar_en_csv(self) -> None:
        """Escribe el estado actual del repositorio en el archivo CSV."""
        if not self._archivo_csv:
            return

        os.makedirs(os.path.dirname(os.path.abspath(self._archivo_csv)), exist_ok=True)
        if not self._datos:
            # Si el diccionario está vacío, limpiamos el archivo CSV para reflejar que no hay datos.
            open(self._archivo_csv, mode="w", encoding="utf-8").close()
            return

        # Obtener nombres de columnas desde la primera entidad
        primera_entidad = next(iter(self._datos.values()))
        columnas = list(primera_entidad.to_dict().keys())

        with open(self._archivo_csv, mode="w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=columnas)
            escritor.writeheader()
            for entidad in self._datos.values():
                escritor.writerow(entidad.to_dict())

    def crear(self, entidad: T) -> T:
        if entidad.id is not None:
            if entidad.id in self._datos:
                raise ValueError(f"Ya existe una entidad con el ID {entidad.id}.")
            if entidad.id >= self._siguiente_id:
                self._siguiente_id = entidad.id + 1
        else:
            entidad.id = self._siguiente_id
            self._siguiente_id += 1

        self._datos[entidad.id] = entidad
        self.guardar_en_csv()
        return entidad

    def leer_por_id(self, id: int) -> Optional[T]:
        return self._datos.get(id)

    def leer_todos(self) -> List[T]:
        return list(self._datos.values())

    def actualizar(self, entidad: T) -> T:
        if entidad.id is None or entidad.id not in self._datos:
            raise ValueError(f"No se encuentra la entidad con ID {entidad.id} para actualizar.")
        self._datos[entidad.id] = entidad
        self.guardar_en_csv()
        return entidad

    def eliminar(self, id: int) -> bool:
        if id in self._datos:
            del self._datos[id]
            self.guardar_en_csv()
            return True
        return False

    def vaciar(self) -> None:
        """Limpia todos los registros del repositorio."""
        self._datos.clear()
        self._siguiente_id = 1


class RepositorioLibro(RepositorioBase[Libro]):
    """Repositorio para la entidad Libro con búsquedas especializadas."""

    def buscar_por_isbn(self, isbn: str) -> Optional[Libro]:
        isbn_normalizado = isbn.strip().lower()
        for libro in self._datos.values():
            if libro.isbn.strip().lower() == isbn_normalizado:
                return libro
        return None

    def buscar_por_titulo(self, termino: str) -> List[Libro]:
        termino_normalizado = termino.strip().lower()
        return [
            libro for libro in self._datos.values()
            if termino_normalizado in libro.titulo.lower()
        ]

    def buscar_por_autor(self, autor: str) -> List[Libro]:
        autor_normalizado = autor.strip().lower()
        return [
            libro for libro in self._datos.values()
            if autor_normalizado in libro.autor.lower()
        ]

    def buscar_por_genero(self, id_genero: int) -> List[Libro]:
        return [libro for libro in self._datos.values() if libro.id_genero == id_genero]

    def buscar_por_editorial(self, id_editorial: int) -> List[Libro]:
        return [libro for libro in self._datos.values() if libro.id_editorial == id_editorial]


class RepositorioGenero(RepositorioBase[Genero]):
    """Repositorio para la entidad Genero."""

    def buscar_por_nombre(self, nombre: str) -> Optional[Genero]:
        nombre_normalizado = nombre.strip().lower()
        for genero in self._datos.values():
            if genero.nombre.strip().lower() == nombre_normalizado:
                return genero
        return None


class RepositorioEditorial(RepositorioBase[Editorial]):
    """Repositorio para la entidad Editorial."""

    def buscar_por_nombre(self, nombre: str) -> Optional[Editorial]:
        nombre_normalizado = nombre.strip().lower()
        for editorial in self._datos.values():
            if editorial.nombre.strip().lower() == nombre_normalizado:
                return editorial
        return None


class RepositorioMoneda(RepositorioBase[Moneda]):
    """Repositorio para la entidad Moneda."""

    def buscar_por_codigo(self, codigo: str) -> Optional[Moneda]:
        codigo_normalizado = codigo.strip().upper()
        for moneda in self._datos.values():
            if moneda.codigo == codigo_normalizado:
                return moneda
        return None


class RepositorioTipoCotizacion(RepositorioBase[TipoCotizacion]):
    """Repositorio para la entidad TipoCotizacion."""

    def buscar_por_nombre(self, nombre: str) -> Optional[TipoCotizacion]:
        nombre_normalizado = nombre.strip().lower()
        for tipo in self._datos.values():
            if tipo.nombre.strip().lower() == nombre_normalizado:
                return tipo
        return None


class RepositorioPrecio(RepositorioBase[Precio]):
    """Repositorio para la entidad Precio."""

    def leer_por_libro_y_moneda(self, id_libro: int, id_moneda: int) -> Optional[Precio]:
        for precio in self._datos.values():
            if precio.id_libro == id_libro and precio.id_moneda == id_moneda:
                return precio
        return None

    def leer_por_libro(self, id_libro: int) -> List[Precio]:
        return [p for p in self._datos.values() if p.id_libro == id_libro]

    def eliminar_por_libro_y_moneda(self, id_libro: int, id_moneda: int) -> bool:
        precio = self.leer_por_libro_y_moneda(id_libro, id_moneda)
        if precio is not None and precio.id is not None:
            return self.eliminar(precio.id)
        return False


class RepositorioStock(RepositorioBase[Stock], IRepositorioStock):
    """Repositorio para la entidad Stock cumpliendo con IRepositorio e IRepositorioStock."""

    def crear(self, stock: Stock) -> Stock:
        if self.leer_por_libro(stock.id_libro) is not None:
            raise ValueError(f"Ya existe un registro de stock para el libro con ID {stock.id_libro}.")
        return super().crear(stock)

    def leer_por_libro(self, libro_id: int) -> Optional[Stock]:
        for stock in self._datos.values():
            if stock.id_libro == libro_id:
                return stock
        return None

    def actualizar(self, stock: Stock) -> Stock:
        stock_existente = self.leer_por_libro(stock.id_libro)
        if stock_existente is None:
            raise ValueError(f"No se encuentra el stock para el libro ID {stock.id_libro} para actualizar.")
        if stock.id is None:
            stock.id = stock_existente.id
        self._datos[stock.id] = stock
        self.guardar_en_csv()
        return stock

    def eliminar(self, libro_id: int) -> bool:
        stock_existente = self.leer_por_libro(libro_id)
        if stock_existente is not None and stock_existente.id is not None:
            return super().eliminar(stock_existente.id)
        return False


class RepositorioCotizacionDolar(RepositorioBase[CotizacionDolar], IRepositorioCotizacionDolar):
    """Repositorio para la entidad CotizacionDolar cumpliendo con IRepositorio e IRepositorioCotizacionDolar."""

    def _normalizar_fecha(self, fecha: Union[date, str]) -> date:
        if isinstance(fecha, str):
            return datetime.strptime(fecha.strip(), "%Y-%m-%d").date()
        return fecha

    def crear(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        fecha_norm = self._normalizar_fecha(cotizacion.fecha)
        if self.leer_por_tipo_y_fecha(cotizacion.id_tipo, fecha_norm) is not None:
            raise ValueError(
                f"Ya existe una cotización para el tipo {cotizacion.id_tipo} en la fecha {fecha_norm}."
            )
        return super().crear(cotizacion)

    def leer_por_tipo_y_fecha(self, tipo_id: int, fecha: Union[date, str]) -> Optional[CotizacionDolar]:
        fecha_norm = self._normalizar_fecha(fecha)
        for cot in self._datos.values():
            if cot.id_tipo == tipo_id and cot.fecha == fecha_norm:
                return cot
        return None

    def leer_historico_por_tipo(self, tipo_id: int) -> List[CotizacionDolar]:
        registros = [cot for cot in self._datos.values() if cot.id_tipo == tipo_id]
        return sorted(registros, key=lambda c: c.fecha)

    def leer_ultima_cotizacion(self, tipo_id: int) -> Optional[CotizacionDolar]:
        historico = self.leer_historico_por_tipo(tipo_id)
        return historico[-1] if historico else None

    def actualizar(self, cotizacion: CotizacionDolar) -> CotizacionDolar:
        fecha_norm = self._normalizar_fecha(cotizacion.fecha)
        cot_existente = self.leer_por_tipo_y_fecha(cotizacion.id_tipo, fecha_norm)
        if cot_existente is None:
            raise ValueError(
                f"No se encuentra la cotización para el tipo {cotizacion.id_tipo} en fecha {fecha_norm} para actualizar."
            )
        if cotizacion.id is None:
            cotizacion.id = cot_existente.id
        self._datos[cotizacion.id] = cotizacion
        self.guardar_en_csv()
        return cotizacion

    def eliminar(self, tipo_id: int, fecha: Union[date, str]) -> bool:
        fecha_norm = self._normalizar_fecha(fecha)
        cot_existente = self.leer_por_tipo_y_fecha(tipo_id, fecha_norm)
        if cot_existente is not None and cot_existente.id is not None:
            return super().eliminar(cot_existente.id)
        return False
