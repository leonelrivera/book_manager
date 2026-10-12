# Book Manager - Sprint 2

## 📌 Objetivo
El objetivo principal de este sprint es consolidar las bases del manejo de bases de datos relacionales, normalización de datos, conexión segura y carga inicial. Se amplía el alcance de la aplicación migrando la persistencia desde archivos planos (CSV) hacia una base de datos relacional mediante el ORM **SQLAlchemy**, además de incorporar la integración con APIs externas para la consulta y actualización de cotizaciones de divisas en tiempo real.

---

## 📖 Introducción y Contexto del Sprint de Trabajo
En esta segunda entrega del proyecto integrador, la librería moderniza su arquitectura tecnológica migrando su capa de persistencia de archivos a tablas relacionales gestionadas por un motor de base de datos relacional (PostgreSQL / Supabase / SQLite).

Se abordan las siguientes áreas clave:
* **Persistencia Relacional con ORM:** Mapeo de entidades a modelos relacionales de SQLAlchemy con claves primarias, foráneas, restricciones de unicidad e integridad referencial.
* **Gestión Segura de Conexiones:** Centralización de la conexión (`ConexionDB`) y control de transacciones atómicas mediante gestores de contexto (`Context Manager`).
* **Migración de Datos:** Procedimiento automatizado para transformar los datos precargados en CSV hacia sentencias `.sql` y poblar la base de datos garantizando la integridad de las relaciones.
* **Integración con Servicios Externos:** Conexión a la API pública de cotizaciones de divisas (`DolarAPI`) utilizando variables de entorno (`.env`) para cotización multimoneda en tiempo real.
* **Reportes y Operaciones Bimonetarias:** Nuevas funcionalidades de consola para visualizar catálogos bimonetarios y exportación de listas de precios actualizadas.

