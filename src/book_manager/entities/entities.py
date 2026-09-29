"""Entidades del dominio para el sistema Book Manager.

Módulo que define las entidades principales de datos con encapsulamiento estricto,
relaciones orientadas a objetos (asociación y composición de instancias),
validaciones en setters, métodos de representación y serialización para CSV.
"""

from abc import ABC
from datetime import date, datetime
from typing import Any, Dict, Optional, Union


class EntidadBase(ABC):
    """Clase base abstracta para todas las entidades del dominio."""

    def __init__(self, id_entidad: Optional[int] = None) -> None:
        self._id: Optional[int] = None
        if id_entidad is not None:
            self.id = id_entidad

    @property
    def id(self) -> Optional[int]:
        """Obtiene el identificador único de la entidad."""
        return self._id

    @id.setter
    def id(self, nuevo_id: Optional[int]) -> None:
        """Establece el identificador único de la entidad con validación."""
        if nuevo_id is not None:
            if not isinstance(nuevo_id, int) or nuevo_id <= 0:
                raise ValueError("El ID debe ser un entero positivo.")
        self._id = nuevo_id

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, self.__class__):
            return False
        if self._id is not None and otro._id is not None:
            return self._id == otro._id
        return False


class Genero(EntidadBase):
    """Categoría literaria a la que pertenece un libro."""

    def __init__(self, id_genero: Optional[int], nombre: str, descripcion: str = "") -> None:
        super().__init__(id_genero)
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def id_genero(self) -> Optional[int]:
        """Alias para el ID del género."""
        return self.id

    @id_genero.setter
    def id_genero(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre del género no puede estar vacío.")
        self.__nombre = nuevo_nombre.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, nueva_descripcion: str) -> None:
        self.__descripcion = str(nueva_descripcion).strip() if nueva_descripcion else ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Genero":
        return cls(
            id_genero=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            nombre=str(data["nombre"]),
            descripcion=str(data.get("descripcion", "")),
        )

    def __repr__(self) -> str:
        return f"Genero(id={self.id}, nombre='{self.nombre}')"


class Editorial(EntidadBase):
    """Proveedor/distribuidora que provee los libros a la librería."""

    def __init__(
        self,
        id_editorial: Optional[int],
        nombre: str,
        pais: str = "Argentina",
        contacto: str = "",
    ) -> None:
        super().__init__(id_editorial)
        self.nombre = nombre
        self.pais = pais
        self.contacto = contacto

    @property
    def id_editorial(self) -> Optional[int]:
        """Alias para el ID de la editorial."""
        return self.id

    @id_editorial.setter
    def id_editorial(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre de la editorial no puede estar vacío.")
        self.__nombre = nuevo_nombre.strip()

    @property
    def pais(self) -> str:
        return self.__pais

    @pais.setter
    def pais(self, nuevo_pais: str) -> None:
        self.__pais = str(nuevo_pais).strip() if nuevo_pais else "Argentina"

    @property
    def contacto(self) -> str:
        return self.__contacto

    @contacto.setter
    def contacto(self, nuevo_contacto: str) -> None:
        self.__contacto = str(nuevo_contacto).strip() if nuevo_contacto else ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "pais": self.pais,
            "contacto": self.contacto,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Editorial":
        return cls(
            id_editorial=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            nombre=str(data["nombre"]),
            pais=str(data.get("pais", "Argentina")),
            contacto=str(data.get("contacto", "")),
        )

    def __repr__(self) -> str:
        return f"Editorial(id={self.id}, nombre='{self.nombre}', pais='{self.pais}')"


class Moneda(EntidadBase):
    """Las distintas monedas en las que se puede expresar un precio (ARS, USD, etc.)."""

    def __init__(
        self,
        id_moneda: Optional[int],
        codigo: str,
        nombre: str,
        simbolo: str = "$",
    ) -> None:
        super().__init__(id_moneda)
        self.codigo = codigo
        self.nombre = nombre
        self.simbolo = simbolo

    @property
    def id_moneda(self) -> Optional[int]:
        """Alias para el ID de la moneda."""
        return self.id

    @id_moneda.setter
    def id_moneda(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, nuevo_codigo: str) -> None:
        if not isinstance(nuevo_codigo, str) or not nuevo_codigo.strip():
            raise ValueError("El código de la moneda no puede estar vacío.")
        self.__codigo = nuevo_codigo.strip().upper()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre de la moneda no puede estar vacío.")
        self.__nombre = nuevo_nombre.strip()

    @property
    def simbolo(self) -> str:
        return self.__simbolo

    @simbolo.setter
    def simbolo(self, nuevo_simbolo: str) -> None:
        self.__simbolo = str(nuevo_simbolo).strip() if nuevo_simbolo else "$"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "simbolo": self.simbolo,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Moneda":
        return cls(
            id_moneda=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            codigo=str(data["codigo"]),
            nombre=str(data["nombre"]),
            simbolo=str(data.get("simbolo", "$")),
        )

    def __repr__(self) -> str:
        return f"Moneda(id={self.id}, codigo='{self.codigo}', nombre='{self.nombre}', simbolo='{self.simbolo}')"


class TipoCotizacion(EntidadBase):
    """Los distintos tipos de cotización del dólar (Oficial, Blue, MEP, etc.)."""

    def __init__(self, id_tipo: Optional[int], nombre: str, descripcion: str = "") -> None:
        super().__init__(id_tipo)
        self.nombre = nombre
        self.descripcion = descripcion

    @property
    def id_tipo(self) -> Optional[int]:
        """Alias para el ID del tipo de cotización."""
        return self.id

    @id_tipo.setter
    def id_tipo(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not isinstance(nuevo_nombre, str) or not nuevo_nombre.strip():
            raise ValueError("El nombre del tipo de cotización no puede estar vacío.")
        self.__nombre = nuevo_nombre.strip()

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, nueva_descripcion: str) -> None:
        self.__descripcion = str(nueva_descripcion).strip() if nueva_descripcion else ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TipoCotizacion":
        return cls(
            id_tipo=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            nombre=str(data["nombre"]),
            descripcion=str(data.get("descripcion", "")),
        )

    def __repr__(self) -> str:
        return f"TipoCotizacion(id={self.id}, nombre='{self.nombre}')"


class Libro(EntidadBase):
    """Representa cada título del catálogo de la librería, compuesto por objetos Género y Editorial."""

    def __init__(
        self,
        id_libro: Optional[int] = None,
        isbn: str = "",
        titulo: str = "",
        autor: str = "",
        genero: Optional[Union[Genero, int]] = None,
        editorial: Optional[Union[Editorial, int]] = None,
        anio_publicacion: Optional[int] = None,
        paginas: Optional[int] = None,
    ) -> None:
        super().__init__(id_libro)
        if genero is None or editorial is None:
            raise ValueError("Debe especificarse el género y la editorial.")
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.editorial = editorial
        self.anio_publicacion = anio_publicacion
        self.paginas = paginas

    @property
    def id_libro(self) -> Optional[int]:
        """Alias para el ID del libro."""
        return self.id

    @id_libro.setter
    def id_libro(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def isbn(self) -> str:
        return self.__isbn

    @isbn.setter
    def isbn(self, nuevo_isbn: str) -> None:
        if not isinstance(nuevo_isbn, str) or not nuevo_isbn.strip():
            raise ValueError("El ISBN no puede estar vacío.")
        self.__isbn = nuevo_isbn.strip()

    @property
    def titulo(self) -> str:
        return self.__titulo

    @titulo.setter
    def titulo(self, nuevo_titulo: str) -> None:
        if not isinstance(nuevo_titulo, str) or not nuevo_titulo.strip():
            raise ValueError("El título no puede estar vacío.")
        self.__titulo = nuevo_titulo.strip()

    @property
    def autor(self) -> str:
        return self.__autor

    @autor.setter
    def autor(self, nuevo_autor: str) -> None:
        if not isinstance(nuevo_autor, str) or not nuevo_autor.strip():
            raise ValueError("El autor no puede estar vacío.")
        self.__autor = nuevo_autor.strip()

    @property
    def genero(self) -> Genero:
        """Objeto Genero asociado al libro (POO pura)."""
        return self.__genero

    @genero.setter
    def genero(self, nuevo_genero: Union[Genero, int]) -> None:
        if isinstance(nuevo_genero, Genero):
            self.__genero = nuevo_genero
        elif isinstance(nuevo_genero, int) and nuevo_genero > 0:
            self.__genero = Genero(id_genero=nuevo_genero, nombre=f"Genero #{nuevo_genero}")
        else:
            raise ValueError("El género debe ser una instancia de Genero o un ID entero positivo.")

    @property
    def id_genero(self) -> int:
        """ID del género obtenido a través del objeto Genero."""
        return self.genero.id if self.genero and self.genero.id is not None else 1

    @id_genero.setter
    def id_genero(self, nuevo_id_genero: int) -> None:
        self.genero = nuevo_id_genero

    @property
    def editorial(self) -> Editorial:
        """Objeto Editorial asociado al libro (POO pura)."""
        return self.__editorial

    @editorial.setter
    def editorial(self, nueva_editorial: Union[Editorial, int]) -> None:
        if isinstance(nueva_editorial, Editorial):
            self.__editorial = nueva_editorial
        elif isinstance(nueva_editorial, int) and nueva_editorial > 0:
            self.__editorial = Editorial(id_editorial=nueva_editorial, nombre=f"Editorial #{nueva_editorial}")
        else:
            raise ValueError("La editorial debe ser una instancia de Editorial o un ID entero positivo.")

    @property
    def id_editorial(self) -> int:
        """ID de la editorial obtenido a través del objeto Editorial."""
        return self.editorial.id if self.editorial and self.editorial.id is not None else 1

    @id_editorial.setter
    def id_editorial(self, nuevo_id_editorial: int) -> None:
        self.editorial = nuevo_id_editorial

    @property
    def anio_publicacion(self) -> Optional[int]:
        return self.__anio_publicacion

    @anio_publicacion.setter
    def anio_publicacion(self, anio: Optional[int]) -> None:
        if anio is not None and (not isinstance(anio, int) or anio < 0 or anio > 2100):
            raise ValueError("El año de publicación debe ser un año válido.")
        self.__anio_publicacion = anio

    @property
    def paginas(self) -> Optional[int]:
        return self.__paginas

    @paginas.setter
    def paginas(self, num_paginas: Optional[int]) -> None:
        if num_paginas is not None and (not isinstance(num_paginas, int) or num_paginas <= 0):
            raise ValueError("El número de páginas debe ser un entero positivo.")
        self.__paginas = num_paginas

    def to_dict(self) -> Dict[str, Any]:
        """Serializa la entidad a diccionario extrayendo las claves foráneas desde los objetos."""
        return {
            "id": self.id,
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "id_genero": self.id_genero,
            "id_editorial": self.id_editorial,
            "anio_publicacion": self.anio_publicacion,
            "paginas": self.paginas,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Libro":
        return cls(
            id_libro=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            isbn=str(data["isbn"]),
            titulo=str(data["titulo"]),
            autor=str(data["autor"]),
            genero=int(data["id_genero"]),
            editorial=int(data["id_editorial"]),
            anio_publicacion=int(data["anio_publicacion"]) if data.get("anio_publicacion") and str(data["anio_publicacion"]).strip() else None,
            paginas=int(data["paginas"]) if data.get("paginas") and str(data["paginas"]).strip() else None,
        )

    def __repr__(self) -> str:
        gen_nom = self.genero.nombre if self.genero else "N/A"
        ed_nom = self.editorial.nombre if self.editorial else "N/A"
        return f"Libro(id={self.id}, isbn='{self.isbn}', titulo='{self.titulo}', autor='{self.autor}', genero='{gen_nom}', editorial='{ed_nom}')"


class Precio(EntidadBase):
    """Valor monetario asociado a un libro en una moneda determinada."""

    def __init__(
        self,
        id_precio: Optional[int] = None,
        libro: Optional[Union[Libro, int]] = None,
        moneda: Optional[Union[Moneda, int]] = None,
        valor: float = 0.0,
        id_libro: Optional[int] = None,
        id_moneda: Optional[int] = None,
    ) -> None:
        super().__init__(id_precio)
        libro_final = libro if libro is not None else id_libro
        moneda_final = moneda if moneda is not None else id_moneda
        if libro_final is None or moneda_final is None:
            raise ValueError("Debe especificarse el libro y la moneda.")
        self.libro = libro_final
        self.moneda = moneda_final
        self.valor = valor

    @property
    def id_precio(self) -> Optional[int]:
        """Alias para el ID del precio."""
        return self.id

    @id_precio.setter
    def id_precio(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def libro(self) -> Union[Libro, int]:
        return self.__libro

    @libro.setter
    def libro(self, nuevo_libro: Union[Libro, int]) -> None:
        if isinstance(nuevo_libro, (Libro, int)):
            self.__libro = nuevo_libro
        else:
            raise ValueError("El libro debe ser una instancia de Libro o un ID entero.")

    @property
    def id_libro(self) -> int:
        if isinstance(self.__libro, Libro):
            return self.__libro.id or 1
        return self.__libro

    @id_libro.setter
    def id_libro(self, nuevo_id: int) -> None:
        self.libro = nuevo_id

    @property
    def moneda(self) -> Union[Moneda, int]:
        return self.__moneda

    @moneda.setter
    def moneda(self, nueva_moneda: Union[Moneda, int]) -> None:
        if isinstance(nueva_moneda, (Moneda, int)):
            self.__moneda = nueva_moneda
        else:
            raise ValueError("La moneda debe ser una instancia de Moneda o un ID entero.")

    @property
    def id_moneda(self) -> int:
        if isinstance(self.__moneda, Moneda):
            return self.__moneda.id or 1
        return self.__moneda

    @id_moneda.setter
    def id_moneda(self, nuevo_id: int) -> None:
        self.moneda = nuevo_id

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, nuevo_valor: Union[float, int]) -> None:
        if not isinstance(nuevo_valor, (int, float)) or nuevo_valor < 0:
            raise ValueError("El valor del precio debe ser un número mayor o igual a 0.")
        self.__valor = float(nuevo_valor)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "id_libro": self.id_libro,
            "id_moneda": self.id_moneda,
            "valor": self.valor,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Precio":
        return cls(
            id_precio=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            libro=int(data["id_libro"]),
            moneda=int(data["id_moneda"]),
            valor=float(data["valor"]),
        )

    def __repr__(self) -> str:
        return f"Precio(id={self.id}, id_libro={self.id_libro}, id_moneda={self.id_moneda}, valor={self.valor:.2f})"


class Stock(EntidadBase):
    """Cantidad disponible de cada libro en el inventario."""

    def __init__(
        self,
        id_stock: Optional[int] = None,
        libro: Optional[Union[Libro, int]] = None,
        cantidad: int = 0,
        ubicacion: str = "Depósito Central",
        id_libro: Optional[int] = None,
        libro_id: Optional[int] = None,
    ) -> None:
        super().__init__(id_stock)
        libro_final = libro if libro is not None else (id_libro if id_libro is not None else libro_id)
        if libro_final is None:
            raise ValueError("Debe especificarse el libro para el stock.")
        self.libro = libro_final
        self.cantidad = cantidad
        self.ubicacion = ubicacion

    @property
    def id_stock(self) -> Optional[int]:
        """Alias para el ID del stock."""
        return self.id

    @id_stock.setter
    def id_stock(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def libro(self) -> Union[Libro, int]:
        return self.__libro

    @libro.setter
    def libro(self, nuevo_libro: Union[Libro, int]) -> None:
        if isinstance(nuevo_libro, (Libro, int)):
            self.__libro = nuevo_libro
        else:
            raise ValueError("El libro debe ser una instancia de Libro o un ID entero.")

    @property
    def id_libro(self) -> int:
        if isinstance(self.__libro, Libro):
            return self.__libro.id or 1
        return self.__libro

    @id_libro.setter
    def id_libro(self, nuevo_id_libro: int) -> None:
        self.libro = nuevo_id_libro

    @property
    def libro_id(self) -> int:
        return self.id_libro

    @libro_id.setter
    def libro_id(self, nuevo_id: int) -> None:
        self.id_libro = nuevo_id

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad: int) -> None:
        if not isinstance(nueva_cantidad, int) or nueva_cantidad < 0:
            raise ValueError("La cantidad de stock debe ser un entero mayor o igual a 0.")
        self.__cantidad = nueva_cantidad

    @property
    def ubicacion(self) -> str:
        return self.__ubicacion

    @ubicacion.setter
    def ubicacion(self, nueva_ubicacion: str) -> None:
        self.__ubicacion = str(nueva_ubicacion).strip() if nueva_ubicacion else "Depósito Central"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "id_libro": self.id_libro,
            "cantidad": self.cantidad,
            "ubicacion": self.ubicacion,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Stock":
        return cls(
            id_stock=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            libro=int(data["id_libro"]),
            cantidad=int(data.get("cantidad", 0)),
            ubicacion=str(data.get("ubicacion", "Depósito Central")),
        )

    def __repr__(self) -> str:
        return f"Stock(id={self.id}, id_libro={self.id_libro}, cantidad={self.cantidad}, ubicacion='{self.ubicacion}')"


class CotizacionDolar(EntidadBase):
    """Registro histórico de las cotizaciones del dólar por tipo y fecha."""

    def __init__(
        self,
        id_cotizacion: Optional[int] = None,
        tipo: Optional[Union[TipoCotizacion, int]] = None,
        fecha: Optional[Union[date, str]] = None,
        compra: float = 0.0,
        venta: float = 0.0,
        id_tipo: Optional[int] = None,
        tipo_cotizacion: Optional[Union[TipoCotizacion, int]] = None,
    ) -> None:
        super().__init__(id_cotizacion)
        tipo_final = tipo if tipo is not None else (tipo_cotizacion if tipo_cotizacion is not None else id_tipo)
        if tipo_final is None:
            raise ValueError("Debe especificarse el tipo de cotización.")
        self.tipo = tipo_final
        if fecha is None:
            raise ValueError("Debe especificarse la fecha de la cotización.")
        self.fecha = fecha
        self.compra = compra
        self.venta = venta

    @property
    def id_cotizacion(self) -> Optional[int]:
        """Alias para el ID de la cotización."""
        return self.id

    @id_cotizacion.setter
    def id_cotizacion(self, nuevo_id: Optional[int]) -> None:
        self.id = nuevo_id

    @property
    def tipo(self) -> Union[TipoCotizacion, int]:
        return self.__tipo

    @tipo.setter
    def tipo(self, nuevo_tipo: Union[TipoCotizacion, int]) -> None:
        if isinstance(nuevo_tipo, (TipoCotizacion, int)):
            self.__tipo = nuevo_tipo
        else:
            raise ValueError("El tipo debe ser una instancia de TipoCotizacion o un ID entero.")

    @property
    def id_tipo(self) -> int:
        if isinstance(self.__tipo, TipoCotizacion):
            return self.__tipo.id or 1
        return self.__tipo

    @id_tipo.setter
    def id_tipo(self, nuevo_id_tipo: int) -> None:
        self.tipo = nuevo_id_tipo

    @property
    def tipo_id(self) -> int:
        return self.id_tipo

    @tipo_id.setter
    def tipo_id(self, nuevo_id: int) -> None:
        self.id_tipo = nuevo_id

    @property
    def fecha(self) -> date:
        return self.__fecha

    @fecha.setter
    def fecha(self, nueva_fecha: Union[date, str]) -> None:
        if isinstance(nueva_fecha, str):
            try:
                self.__fecha = datetime.strptime(nueva_fecha.strip(), "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("La fecha debe tener el formato YYYY-MM-DD.")
        elif isinstance(nueva_fecha, datetime):
            self.__fecha = nueva_fecha.date()
        elif isinstance(nueva_fecha, date):
            self.__fecha = nueva_fecha
        else:
            raise TypeError("La fecha debe ser de tipo datetime.date o un string 'YYYY-MM-DD'.")

    @property
    def compra(self) -> float:
        return self.__compra

    @compra.setter
    def compra(self, nuevo_valor: Union[float, int]) -> None:
        if not isinstance(nuevo_valor, (int, float)) or nuevo_valor < 0:
            raise ValueError("El valor de compra debe ser un número mayor o igual a 0.")
        self.__compra = float(nuevo_valor)

    @property
    def venta(self) -> float:
        return self.__venta

    @venta.setter
    def venta(self, nuevo_valor: Union[float, int]) -> None:
        if not isinstance(nuevo_valor, (int, float)) or nuevo_valor < 0:
            raise ValueError("El valor de venta debe ser un número mayor o igual a 0.")
        self.__venta = float(nuevo_valor)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "id_tipo": self.id_tipo,
            "fecha": self.fecha.strftime("%Y-%m-%d"),
            "compra": self.compra,
            "venta": self.venta,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CotizacionDolar":
        return cls(
            id_cotizacion=int(data["id"]) if data.get("id") is not None and str(data["id"]).strip() else None,
            tipo=int(data["id_tipo"]),
            fecha=str(data["fecha"]),
            compra=float(data["compra"]),
            venta=float(data["venta"]),
        )

    def __repr__(self) -> str:
        return (
            f"CotizacionDolar(id={self.id}, id_tipo={self.id_tipo}, "
            f"fecha='{self.fecha}', compra={self.compra:.2f}, venta={self.venta:.2f})"
        )


# Alias para compatibilidad con la consigna
Cotizacion = CotizacionDolar