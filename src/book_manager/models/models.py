"""Modelos ORM de SQLAlchemy para el sistema Book Manager.

Define el esquema relacional de la base de datos utilizando el enfoque declarativo
de SQLAlchemy 2.0 (DeclarativeBase), configurando tipos de datos, claves primarias,
claves foráneas, restricciones de integridad y relaciones bidireccionales (relationship)
para navegación orientada a objetos pura.
"""

from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos ORM de SQLAlchemy."""
    pass


class GeneroModel(Base):
    """Modelo ORM para la tabla 'generos'.

    Representa las categorías temáticas y literarias a las que pertenecen los libros.
    """

    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")

    # Relación uno-a-muchos con LibroModel
    libros: Mapped[List["LibroModel"]] = relationship(
        "LibroModel",
        back_populates="genero",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"GeneroModel(id={self.id}, nombre='{self.nombre}')"


class EditorialModel(Base):
    """Modelo ORM para la tabla 'editoriales'.

    Representa los sellos editoriales o distribuidores de los libros.
    """

    __tablename__ = "editoriales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    pais: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="Argentina")
    contacto: Mapped[Optional[str]] = mapped_column(String(150), nullable=True, default="")

    # Relación uno-a-muchos con LibroModel
    libros: Mapped[List["LibroModel"]] = relationship(
        "LibroModel",
        back_populates="editorial",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"EditorialModel(id={self.id}, nombre='{self.nombre}', pais='{self.pais}')"


class MonedaModel(Base):
    """Modelo ORM para la tabla 'monedas'.

    Representa las divisas en las cuales se cotizan o expresan los precios.
    """

    __tablename__ = "monedas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    simbolo: Mapped[str] = mapped_column(String(10), nullable=False, default="$")

    # Relación uno-a-muchos con PrecioModel
    precios: Mapped[List["PrecioModel"]] = relationship(
        "PrecioModel",
        back_populates="moneda",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"MonedaModel(id={self.id}, codigo='{self.codigo}', nombre='{self.nombre}')"


class TipoCotizacionModel(Base):
    """Modelo ORM para la tabla 'tipos_cotizacion'.

    Representa las modalidades o tipos de cotización del dólar (Oficial, Blue, MEP, etc.).
    """

    __tablename__ = "tipos_cotizacion"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")

    # Relación uno-a-muchos con CotizacionDolarModel
    cotizaciones: Mapped[List["CotizacionDolarModel"]] = relationship(
        "CotizacionDolarModel",
        back_populates="tipo_cotizacion",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"TipoCotizacionModel(id={self.id}, nombre='{self.nombre}')"


class LibroModel(Base):
    """Modelo ORM para la tabla 'libros'.

    Representa cada título del catálogo literario, vinculando claves foráneas
    con sus relaciones orientadas a objetos (genero y editorial).
    """

    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    autor: Mapped[str] = mapped_column(String(255), nullable=False)
    anio_publicacion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    paginas: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Claves foráneas
    id_genero: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("generos.id", ondelete="CASCADE"),
        nullable=False,
    )
    id_editorial: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("editoriales.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relaciones Muchos-a-Uno (navegación a objetos)
    genero: Mapped["GeneroModel"] = relationship("GeneroModel", back_populates="libros")
    editorial: Mapped["EditorialModel"] = relationship("EditorialModel", back_populates="libros")

    # Relaciones dependientes
    precios: Mapped[List["PrecioModel"]] = relationship(
        "PrecioModel",
        back_populates="libro",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    stock: Mapped[Optional["StockModel"]] = relationship(
        "StockModel",
        back_populates="libro",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            f"LibroModel(id={self.id}, isbn='{self.isbn}', titulo='{self.titulo}', "
            f"autor='{self.autor}', id_genero={self.id_genero}, id_editorial={self.id_editorial})"
        )


class PrecioModel(Base):
    """Modelo ORM para la tabla 'precios'.

    Representa el valor monetario de un libro expresado en una moneda determinada.
    """

    __tablename__ = "precios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    valor: Mapped[float] = mapped_column(Float, nullable=False)

    # Claves foráneas
    id_libro: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("libros.id", ondelete="CASCADE"),
        nullable=False,
    )
    id_moneda: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("monedas.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relaciones Muchos-a-Uno
    libro: Mapped["LibroModel"] = relationship("LibroModel", back_populates="precios")
    moneda: Mapped["MonedaModel"] = relationship("MonedaModel", back_populates="precios")

    def __repr__(self) -> str:
        return f"PrecioModel(id={self.id}, id_libro={self.id_libro}, id_moneda={self.id_moneda}, valor={self.valor})"


class StockModel(Base):
    """Modelo ORM para la tabla 'stock'.

    Representa las existencias físicas y la ubicación de almacenamiento de cada libro.
    """

    __tablename__ = "stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ubicacion: Mapped[str] = mapped_column(String(150), nullable=False, default="Depósito Central")

    # Clave foránea (1-a-1 con libro)
    id_libro: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("libros.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Relación Uno-a-Uno
    libro: Mapped["LibroModel"] = relationship("LibroModel", back_populates="stock")

    def __repr__(self) -> str:
        return f"StockModel(id={self.id}, id_libro={self.id_libro}, cantidad={self.cantidad}, ubicacion='{self.ubicacion}')"


class CotizacionDolarModel(Base):
    """Modelo ORM para la tabla 'cotizaciones'.

    Almacena los registros históricos y actuales de cotizaciones de divisas.
    """

    __tablename__ = "cotizaciones"
    __table_args__ = (
        UniqueConstraint("id_tipo", "fecha", name="uq_cotizacion_tipo_fecha"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    compra: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    venta: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # Clave foránea
    id_tipo: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tipos_cotizacion.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relación Muchos-a-Uno
    tipo_cotizacion: Mapped["TipoCotizacionModel"] = relationship(
        "TipoCotizacionModel",
        back_populates="cotizaciones",
    )

    def __repr__(self) -> str:
        return (
            f"CotizacionDolarModel(id={self.id}, id_tipo={self.id_tipo}, "
            f"fecha='{self.fecha}', compra={self.compra}, venta={self.venta})"
        )


class AuditoriaModel(Base):
    """Modelo ORM para la tabla 'auditoria'.

    Registra la traza de auditoría de cada operación ejecutada en el sistema.
    Campos requeridos por la consigna (Ejercicio 06):
        - acción (accion)
        - fecha (fecha)
        - detalles (detalles)
    """

    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    accion: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    detalles: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")

    def __repr__(self) -> str:
        resumen = (self.detalles or "")[:30]
        return f"AuditoriaModel(id={self.id}, accion='{self.accion}', fecha='{self.fecha}', detalles='{resumen}...' )"


# Aliases y exportación de modelos
CotizacionModel = CotizacionDolarModel

