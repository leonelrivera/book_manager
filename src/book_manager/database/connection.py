"""Módulo de conexión y gestión transaccional con SQLAlchemy para Book Manager.

Proporciona la clase ConexionDB para administrar el motor de base de datos
(Engine), la fábrica de sesiones (sessionmaker) y la conectividad con Supabase
(PostgreSQL) u otros motores relacionales compatibles con SQLAlchemy.
Además, implementa un gestor de contexto (Context Manager) para transacciones atómicas.
"""

import os
from contextlib import contextmanager
from typing import Generator, Optional
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker


class TransaccionContextManager:
    """Gestor de contexto clásico para administración de transacciones con SQLAlchemy.

    Implementa el protocolo context manager mediante __enter__ y __exit__,
    garantizando commit ante finalización correcta, rollback ante excepciones
    y cierre (close) definitivo de la sesión.
    """

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        """Inicializa el context manager con la fábrica de sesiones.

        Args:
            session_factory: Fábrica sessionmaker vinculada al motor de base de datos.
        """
        self._session_factory = session_factory
        self._session: Optional[Session] = None

    def __enter__(self) -> Session:
        """Abre y entrega una nueva sesión de base de datos.

        Returns:
            Session: Sesión de SQLAlchemy activa.
        """
        self._session = self._session_factory()
        return self._session

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> bool:
        """Controla la finalización de la transacción.

        Aplica commit si no ocurrieron excepciones, o rollback si ocurrió algún error,
        garantizando siempre el cierre de los recursos.

        Args:
            exc_type: Tipo de excepción ocurrida, si existe.
            exc_val: Instancia de la excepción ocurrida, si existe.
            exc_tb: Traceback de la excepción, si existe.

        Returns:
            bool: False para propagar la excepción si ocurrió alguna.
        """
        if self._session is not None:
            try:
                if exc_type is None:
                    self._session.commit()
                else:
                    self._session.rollback()
            finally:
                self._session.close()
        return False


class ConexionDB:
    """Administrador centralizado de la conexión a la base de datos con SQLAlchemy.

    Implementa el patrón Singleton para reutilizar el motor (Engine) y el grupo de
    conexiones (connection pool), soportando configuración mediante variables de entorno
    (.env) para Supabase (PostgreSQL) o almacenamiento local de respaldo (SQLite).
    """

    _instancia: Optional["ConexionDB"] = None

    def __init__(self, database_url: Optional[str] = None) -> None:
        """Inicializa la conexión a la base de datos y la fábrica de sesiones.

        Args:
            database_url: Cadena de conexión opcional. Si no se provee, se obtiene
                de la variable de entorno DATABASE_URL (.env). Si no existe, se
                utiliza una base de datos local SQLite como respaldo.
        """
        load_dotenv()

        if database_url is None:
            database_url = os.getenv("DATABASE_URL", "sqlite:///book_manager.db")

        # Corrección de prefijo para compatibilidad con SQLAlchemy 2.0 y psycopg2
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
        elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

        self._database_url: str = database_url

        # Configuración del motor: pool_pre_ping previene conexiones caídas en servicios cloud como Supabase
        connect_args = {}
        if self._database_url.startswith("sqlite"):
            connect_args["check_same_thread"] = False

        self._engine: Engine = create_engine(
            self._database_url,
            echo=False,
            pool_pre_ping=True,
            connect_args=connect_args,
        )

        self._session_factory: sessionmaker[Session] = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @classmethod
    def get_instancia(cls, database_url: Optional[str] = None) -> "ConexionDB":
        """Obtiene o inicializa la instancia única (Singleton) de ConexionDB.

        Args:
            database_url: Cadena de conexión opcional para inicializar o cambiar.

        Returns:
            ConexionDB: La instancia única de la conexión a la base de datos.
        """
        if cls._instancia is None or database_url is not None:
            cls._instancia = cls(database_url=database_url)
        return cls._instancia

    @property
    def database_url(self) -> str:
        """Retorna la cadena de conexión configurada (sin exponer credenciales sensibles)."""
        return self._database_url

    @property
    def engine(self) -> Engine:
        """Retorna el motor (Engine) de SQLAlchemy."""
        return self._engine

    @property
    def session_factory(self) -> sessionmaker[Session]:
        """Retorna la fábrica de sesiones (sessionmaker) configurada."""
        return self._session_factory

    def crear_sesion(self) -> Session:
        """Crea y retorna una nueva sesión de SQLAlchemy directa.

        Returns:
            Session: Sesión activa para interactuar con la base de datos.
        """
        return self._session_factory()

    def transaccion(self) -> TransaccionContextManager:
        """Proporciona un context manager de transacción atómica basado en clase.

        Ejemplo de uso:
            with conexion.transaccion() as session:
                session.add(nuevo_objeto)

        Returns:
            TransaccionContextManager: Gestor de contexto para la transacción.
        """
        return TransaccionContextManager(self._session_factory)

    @contextmanager
    def obtener_sesion(self) -> Generator[Session, None, None]:
        """Proporciona un gestor de contexto con generador para transacciones seguras.

        Garantiza commit automático al finalizar el bloque without exceptions,
        rollback automático ante cualquier fallo y el cierre seguro de la sesión.

        Yields:
            Session: Sesión de SQLAlchemy activa dentro de la transacción.

        Raises:
            Exception: Relanza cualquier excepción producida tras realizar el rollback.
        """
        session: Session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def probar_conexion(self) -> bool:
        """Verifica la conectividad con la base de datos ejecutando una consulta elemental.

        Returns:
            bool: True si la conexión fue exitosa, False en caso de error.
        """
        try:
            with self._engine.connect() as conexion:
                conexion.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError as error:
            print(f"⚠️ Error al conectar con la base de datos: {error}")
            return False


@contextmanager
def transaccion_db(database_url: Optional[str] = None) -> Generator[Session, None, None]:
    """Función de utilidad global para ejecutar bloques transaccionales.

    Args:
        database_url: Cadena de conexión opcional.

    Yields:
        Session: Sesión transaccional activa.
    """
    conexion = ConexionDB.get_instancia(database_url=database_url)
    with conexion.obtener_sesion() as session:
        yield session
