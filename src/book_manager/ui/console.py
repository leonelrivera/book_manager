"""Interfaz de usuario de consola (CLI) para el sistema Book Manager.

Proporciona menús interactivos mediante coincidencia de patrones (match-case),
visualización en tablas formateadas y operaciones CRUD para cada una de las
entidades del catálogo y reportes.
"""

from typing import Any, Dict, List, Optional

from book_manager.services.services import BookManagerService


class ConsolaUI:
    """Clase principal que orquesta la interfaz de usuario en consola."""

    def __init__(self, book_manager_service: BookManagerService) -> None:
        self.bm = book_manager_service

    # ---------------------------------------------------------
    # Métodos de Formato y Visualización
    # ---------------------------------------------------------
    def imprimir_encabezado(self, titulo: str) -> None:
        linea = "=" * 70
        print(f"\n{linea}")
        print(f" {titulo.center(68)} ")
        print(f"{linea}")

    def imprimir_separador(self, caracter: str = "-", longitud: int = 70) -> None:
        print(caracter * longitud)

    # ---------------------------------------------------------
    # CRUD: LIBRO
    # ---------------------------------------------------------
    def listar_libros(self) -> None:
        self.imprimir_encabezado("CATÁLOGO DE LIBROS")
        libros = self.bm.libro_service.listar_todos()
        if not libros:
            print("No hay libros registrados.")
            return

        print(f"{'ID':<4} | {'ISBN':<17} | {'TÍTULO':<25} | {'AUTOR':<16} | {'GÉN':<3} | {'ED':<3} | {'AÑO':<4} | {'PÁGS':<4}")
        self.imprimir_separador(longitud=95)
        for l in libros:
            anio = l.anio_publicacion if l.anio_publicacion else "-"
            pags = l.paginas if l.paginas else "-"
            print(f"{l.id:<4} | {l.isbn:<17} | {l.titulo[:23]:<25} | {l.autor[:14]:<16} | {l.id_genero:<3} | {l.id_editorial:<3} | {str(anio):<4} | {str(pags):<4}")

    def crear_libro(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        id_genero: int,
        id_editorial: int,
        anio: Optional[int] = None,
        paginas: Optional[int] = None,
    ) -> None:
        try:
            nuevo = self.bm.libro_service.crear_libro(isbn, titulo, autor, id_genero, id_editorial, anio, paginas)
            print(f"✅ Libro creado con éxito: ID={nuevo.id} - '{nuevo.titulo}'")
        except Exception as e:
            print(f"❌ Error al crear libro: {e}")

    def actualizar_libro(
        self,
        id_libro: int,
        isbn: str,
        titulo: str,
        autor: str,
        id_genero: int,
        id_editorial: int,
        anio: Optional[int] = None,
        paginas: Optional[int] = None,
    ) -> None:
        try:
            act = self.bm.libro_service.actualizar_libro(id_libro, isbn, titulo, autor, id_genero, id_editorial, anio, paginas)
            print(f"✅ Libro actualizado: ID={act.id} - '{act.titulo}'")
        except Exception as e:
            print(f"❌ Error al actualizar libro: {e}")

    def eliminar_libro(self, id_libro: int) -> None:
        try:
            if self.bm.libro_service.eliminar_libro(id_libro):
                print(f"✅ Libro ID={id_libro} eliminado correctamente.")
            else:
                print(f"⚠️ No se encontró el libro ID={id_libro}.")
        except Exception as e:
            print(f"❌ Error al eliminar libro: {e}")

    # ---------------------------------------------------------
    # CRUD: GÉNERO
    # ---------------------------------------------------------
    def listar_generos(self) -> None:
        self.imprimir_encabezado("GÉNEROS LITERARIOS")
        generos = self.bm.genero_service.listar_todos()
        if not generos:
            print("No hay géneros registrados.")
            return

        print(f"{'ID':<4} | {'NOMBRE':<25} | {'DESCRIPCIÓN':<35}")
        self.imprimir_separador()
        for g in generos:
            print(f"{g.id:<4} | {g.nombre:<25} | {g.descripcion[:33]:<35}")

    def crear_genero(self, nombre: str, descripcion: str = "") -> None:
        try:
            nuevo = self.bm.genero_service.crear_genero(nombre, descripcion)
            print(f"✅ Género creado: ID={nuevo.id} - '{nuevo.nombre}'")
        except Exception as e:
            print(f"❌ Error al crear género: {e}")

    def actualizar_genero(self, id_genero: int, nombre: str, descripcion: str = "") -> None:
        try:
            act = self.bm.genero_service.actualizar_genero(id_genero, nombre, descripcion)
            print(f"✅ Género actualizado: ID={act.id} - '{act.nombre}'")
        except Exception as e:
            print(f"❌ Error al actualizar género: {e}")

    def eliminar_genero(self, id_genero: int) -> None:
        try:
            if self.bm.genero_service.eliminar_genero(id_genero):
                print(f"✅ Género ID={id_genero} eliminado correctamente.")
            else:
                print(f"⚠️ No se encontró el género ID={id_genero}.")
        except Exception as e:
            print(f"❌ Error al eliminar género: {e}")

    # ---------------------------------------------------------
    # CRUD: EDITORIAL
    # ---------------------------------------------------------
    def listar_editoriales(self) -> None:
        self.imprimir_encabezado("EDITORIALES Y DISTRIBUIDORAS")
        editoriales = self.bm.editorial_service.listar_todas()
        if not editoriales:
            print("No hay editoriales registradas.")
            return

        print(f"{'ID':<4} | {'NOMBRE':<28} | {'PAÍS':<15} | {'CONTACTO':<20}")
        self.imprimir_separador()
        for ed in editoriales:
            print(f"{ed.id:<4} | {ed.nombre:<28} | {ed.pais:<15} | {ed.contacto[:18]:<20}")

    def crear_editorial(self, nombre: str, pais: str = "Argentina", contacto: str = "") -> None:
        try:
            nuevo = self.bm.editorial_service.crear_editorial(nombre, pais, contacto)
            print(f"✅ Editorial creada: ID={nuevo.id} - '{nuevo.nombre}'")
        except Exception as e:
            print(f"❌ Error al crear editorial: {e}")

    def actualizar_editorial(self, id_editorial: int, nombre: str, pais: str = "Argentina", contacto: str = "") -> None:
        try:
            act = self.bm.editorial_service.actualizar_editorial(id_editorial, nombre, pais, contacto)
            print(f"✅ Editorial actualizada: ID={act.id} - '{act.nombre}'")
        except Exception as e:
            print(f"❌ Error al actualizar editorial: {e}")

    def eliminar_editorial(self, id_editorial: int) -> None:
        try:
            if self.bm.editorial_service.eliminar_editorial(id_editorial):
                print(f"✅ Editorial ID={id_editorial} eliminada correctamente.")
            else:
                print(f"⚠️ No se encontró la editorial ID={id_editorial}.")
        except Exception as e:
            print(f"❌ Error al eliminar editorial: {e}")

    # ---------------------------------------------------------
    # CRUD: MONEDA
    # ---------------------------------------------------------
    def listar_monedas(self) -> None:
        self.imprimir_encabezado("MONEDAS REGISTRADAS")
        monedas = self.bm.moneda_service.listar_todas()
        if not monedas:
            print("No hay monedas registradas.")
            return

        print(f"{'ID':<4} | {'CÓDIGO':<8} | {'SÍMBOLO':<8} | {'NOMBRE':<30}")
        self.imprimir_separador()
        for m in monedas:
            print(f"{m.id:<4} | {m.codigo:<8} | {m.simbolo:<8} | {m.nombre:<30}")

    def crear_moneda(self, codigo: str, nombre: str, simbolo: str = "$") -> None:
        try:
            nuevo = self.bm.moneda_service.crear_moneda(codigo, nombre, simbolo)
            print(f"✅ Moneda creada: ID={nuevo.id} - [{nuevo.codigo}] {nuevo.nombre}")
        except Exception as e:
            print(f"❌ Error al crear moneda: {e}")

    def actualizar_moneda(self, id_moneda: int, codigo: str, nombre: str, simbolo: str = "$") -> None:
        try:
            act = self.bm.moneda_service.actualizar_moneda(id_moneda, codigo, nombre, simbolo)
            print(f"✅ Moneda actualizada: ID={act.id} - [{act.codigo}] {act.nombre}")
        except Exception as e:
            print(f"❌ Error al actualizar moneda: {e}")

    def eliminar_moneda(self, id_moneda: int) -> None:
        try:
            if self.bm.moneda_service.eliminar_moneda(id_moneda):
                print(f"✅ Moneda ID={id_moneda} eliminada correctamente.")
            else:
                print(f"⚠️ No se encontró la moneda ID={id_moneda}.")
        except Exception as e:
            print(f"❌ Error al eliminar moneda: {e}")

    # ---------------------------------------------------------
    # CRUD: TIPO DE COTIZACIÓN
    # ---------------------------------------------------------
    def listar_tipos_cotizacion(self) -> None:
        self.imprimir_encabezado("TIPOS DE COTIZACIÓN DEL DÓLAR")
        tipos = self.bm.tipo_cotizacion_service.listar_todos()
        if not tipos:
            print("No hay tipos de cotización registrados.")
            return

        print(f"{'ID':<4} | {'TIPO':<20} | {'DESCRIPCIÓN':<40}")
        self.imprimir_separador()
        for t in tipos:
            print(f"{t.id:<4} | {t.nombre:<20} | {t.descripcion[:38]:<40}")

    def crear_tipo_cotizacion(self, nombre: str, descripcion: str = "") -> None:
        try:
            nuevo = self.bm.tipo_cotizacion_service.crear_tipo(nombre, descripcion)
            print(f"✅ Tipo de cotización creado: ID={nuevo.id} - '{nuevo.nombre}'")
        except Exception as e:
            print(f"❌ Error al crear tipo de cotización: {e}")

    def actualizar_tipo_cotizacion(self, id_tipo: int, nombre: str, descripcion: str = "") -> None:
        try:
            act = self.bm.tipo_cotizacion_service.actualizar_tipo(id_tipo, nombre, descripcion)
            print(f"✅ Tipo de cotización actualizado: ID={act.id} - '{act.nombre}'")
        except Exception as e:
            print(f"❌ Error al actualizar tipo de cotización: {e}")

    def eliminar_tipo_cotizacion(self, id_tipo: int) -> None:
        try:
            if self.bm.tipo_cotizacion_service.eliminar_tipo(id_tipo):
                print(f"✅ Tipo de cotización ID={id_tipo} eliminado correctamente.")
            else:
                print(f"⚠️ No se encontró el tipo de cotización ID={id_tipo}.")
        except Exception as e:
            print(f"❌ Error al eliminar tipo de cotización: {e}")

    # ---------------------------------------------------------
    # CRUD: COTIZACIÓN DÓLAR
    # ---------------------------------------------------------
    def listar_cotizaciones(self) -> None:
        self.imprimir_encabezado("HISTÓRICO DE COTIZACIONES DE DÓLAR")
        cotizaciones = self.bm.cotizacion_service.listar_todas()
        if not cotizaciones:
            print("No hay cotizaciones registradas.")
            return

        print(f"{'ID':<4} | {'TIPO ID':<8} | {'FECHA':<12} | {'COMPRA ($)':<14} | {'VENTA ($)':<14}")
        self.imprimir_separador()
        for c in cotizaciones:
            print(f"{c.id:<4} | {c.id_tipo:<8} | {str(c.fecha):<12} | ${c.compra:<13.2f} | ${c.venta:<13.2f}")

    def registrar_cotizacion(self, id_tipo: int, fecha: str, compra: float, venta: float) -> None:
        try:
            nuevo = self.bm.cotizacion_service.registrar_cotizacion(id_tipo, fecha, compra, venta)
            print(f"✅ Cotización registrada: Tipo {nuevo.id_tipo} en {nuevo.fecha} -> Compra: ${nuevo.compra:.2f} | Venta: ${nuevo.venta:.2f}")
        except Exception as e:
            print(f"❌ Error al registrar cotización: {e}")

    def eliminar_cotizacion(self, id_tipo: int, fecha: str) -> None:
        try:
            if self.bm.cotizacion_service.eliminar_cotizacion(id_tipo, fecha):
                print(f"✅ Cotización para Tipo={id_tipo} en fecha {fecha} eliminada correctamente.")
            else:
                print(f"⚠️ No se encontró cotización para Tipo={id_tipo} en fecha {fecha}.")
        except Exception as e:
            print(f"❌ Error al eliminar cotización: {e}")

    # ---------------------------------------------------------
    # CRUD: PRECIO
    # ---------------------------------------------------------
    def listar_precios(self) -> None:
        self.imprimir_encabezado("LISTA DE PRECIOS POR LIBRO")
        precios = self.bm.precio_service.listar_todos()
        if not precios:
            print("No hay precios registrados.")
            return

        print(f"{'ID':<4} | {'LIBRO ID':<10} | {'MONEDA ID':<10} | {'VALOR':<15}")
        self.imprimir_separador()
        for p in precios:
            print(f"{p.id:<4} | {p.id_libro:<10} | {p.id_moneda:<10} | ${p.valor:<14.2f}")

    def fijar_precio(self, id_libro: int, id_moneda: int, valor: float) -> None:
        try:
            p = self.bm.precio_service.fijar_precio(id_libro, id_moneda, valor)
            print(f"✅ Precio fijado: Libro ID={p.id_libro}, Moneda ID={p.id_moneda} -> ${p.valor:.2f}")
        except Exception as e:
            print(f"❌ Error al fijar precio: {e}")

    def eliminar_precio(self, id_libro: int, id_moneda: int) -> None:
        try:
            if self.bm.precio_service.eliminar_precio(id_libro, id_moneda):
                print(f"✅ Precio de Libro ID={id_libro} en Moneda ID={id_moneda} eliminado correctamente.")
            else:
                print(f"⚠️ No se encontró precio registrado para Libro ID={id_libro} en Moneda ID={id_moneda}.")
        except Exception as e:
            print(f"❌ Error al eliminar precio: {e}")

    # ---------------------------------------------------------
    # CRUD: STOCK
    # ---------------------------------------------------------
    def listar_stock(self) -> None:
        self.imprimir_encabezado("CONTROL DE STOCK E INVENTARIO")
        stock_list = self.bm.stock_service.listar_todo()
        if not stock_list:
            print("No hay registros de stock.")
            return

        print(f"{'ID':<4} | {'LIBRO ID':<10} | {'CANTIDAD':<10} | {'UBICACIÓN':<25}")
        self.imprimir_separador()
        for s in stock_list:
            print(f"{s.id:<4} | {s.id_libro:<10} | {s.cantidad:<10} | {s.ubicacion:<25}")

    def asignar_stock(self, id_libro: int, cantidad: int, ubicacion: str = "Depósito Central") -> None:
        try:
            s = self.bm.stock_service.registrar_stock_inicial(id_libro, cantidad, ubicacion)
            print(f"✅ Stock asignado: Libro ID={s.id_libro} -> {s.cantidad} unidades ({s.ubicacion})")
        except Exception as e:
            print(f"❌ Error al asignar stock: {e}")

    def incrementar_stock(self, id_libro: int, cantidad: int) -> None:
        try:
            s = self.bm.stock_service.incrementar_stock(id_libro, cantidad)
            print(f"✅ Stock incrementado: Libro ID={s.id_libro} -> Total: {s.cantidad} unidades")
        except Exception as e:
            print(f"❌ Error al incrementar stock: {e}")

    def decrementar_stock(self, id_libro: int, cantidad: int) -> None:
        try:
            s = self.bm.stock_service.decrementar_stock(id_libro, cantidad)
            print(f"✅ Stock decrementado: Libro ID={s.id_libro} -> Total: {s.cantidad} unidades")
        except Exception as e:
            print(f"❌ Error al decrementar stock: {e}")

    def eliminar_stock(self, id_libro: int) -> None:
        try:
            if self.bm.stock_service.eliminar_stock(id_libro):
                print(f"✅ Registro de stock del Libro ID={id_libro} eliminado correctamente.")
            else:
                print(f"⚠️ No se encontró registro de stock para el Libro ID={id_libro}.")
        except Exception as e:
            print(f"❌ Error al eliminar stock: {e}")

    # ---------------------------------------------------------
    # REPORTES ANALÍTICOS
    # ---------------------------------------------------------
    def mostrar_reporte_catalogo(self, tipo_dolar: str = "Blue") -> None:
        self.imprimir_encabezado(f"REPORTE: CATÁLOGO COMPLETO Y CONVERSIÓN (Dólar {tipo_dolar})")
        catalogo = self.bm.reporte_service.reporte_catalogo_completo(tipo_dolar=tipo_dolar)
        if not catalogo:
            print("El catálogo está vacío.")
            return

        print(f"{'ID':<3} | {'TÍTULO':<25} | {'GÉNERO':<14} | {'EDITORIAL':<16} | {'STOCK':<5} | {'ARS':<10} | {'USD (EST)':<10}")
        self.imprimir_separador()
        for item in catalogo:
            p_ars_str = f"${item['precio_ars']:,.2f}" if item['precio_ars'] is not None else "N/D"
            p_usd_str = f"US${item['precio_usd']:,.2f}" if item['precio_usd'] is not None else "N/D"
            print(
                f"{item['id']:<3} | {item['titulo'][:23]:<25} | {item['genero'][:12]:<14} | "
                f"{item['editorial'][:14]:<16} | {item['stock']:<5} | {p_ars_str:<10} | {p_usd_str:<10}"
            )

    def mostrar_reporte_valorizacion(self, tipo_dolar: str = "Blue") -> None:
        self.imprimir_encabezado("REPORTE: VALORIZACIÓN GLOBAL DEL INVENTARIO")
        val = self.bm.reporte_service.reporte_valorizacion_inventario(tipo_dolar=tipo_dolar)
        print(f"• Total de títulos distintos:    {val['total_titulos']}")
        print(f"• Total de ejemplares en stock:  {val['total_ejemplares']} unidades")
        print(f"• Dólar de referencia:           Dólar {val['tipo_dolar_referencia']}")
        print(f"• Valuación total en ARS:        ${val['valor_total_ars']:,.2f}")
        print(f"• Valuación total en USD:        US${val['valor_total_usd']:,.2f}")
        self.imprimir_separador()

    def mostrar_reporte_stock_critico(self, umbral: int = 5) -> None:
        self.imprimir_encabezado(f"REPORTE: ALERTAS DE STOCK CRÍTICO (<= {umbral} unidades)")
        criticos = self.bm.reporte_service.reporte_stock_critico(umbral=umbral)
        if not criticos:
            print("✅ No hay libros con nivel de stock crítico.")
            return

        for item in criticos:
            print(f"⚠️ [STOCK BAJO: {item['stock']}] Libro ID={item['id']}: '{item['titulo']}' de {item['autor']}")
        self.imprimir_separador()

    def mostrar_reporte_generos(self) -> None:
        self.imprimir_encabezado("REPORTE: DISTRIBUCIÓN DE TÍTULOS POR GÉNERO")
        distribucion = self.bm.reporte_service.reporte_distribucion_generos()
        for genero, cantidad in distribucion.items():
            barra = "█" * cantidad
            print(f"{genero:<25} | {cantidad:>2} títulos {barra}")
        self.imprimir_separador()

    # ---------------------------------------------------------
    # Menú Interactivo de Navegación con Match-Case
    # ---------------------------------------------------------
    def iniciar_menu_interactivo(self) -> None:
        """Menú principal interactivo de consola utilizando coincidencia de patrones (match-case)."""
        while True:
            self.imprimir_encabezado("BOOK MANAGER - MENÚ PRINCIPAL (SPRINT 1)")
            print("1. 📚 Catálogo y Gestión de Libros")
            print("2. 🏷️  Géneros Literarios")
            print("3. 🏢 Editoriales y Distribuidoras")
            print("4. 💵 Monedas y Divisas")
            print("5. 📈 Tipos y Cotizaciones del Dólar")
            print("6. 💰 Lista de Precios")
            print("7. 📦 Control de Stock e Inventario")
            print("8. 📊 Menú de Reportes Analíticos")
            print("0. 🚪 Salir del Sistema")
            self.imprimir_separador()

            opcion = input("Seleccione una opción: ").strip()

            match opcion:
                case "1":
                    self._menu_libros()
                case "2":
                    self._menu_generos()
                case "3":
                    self._menu_editoriales()
                case "4":
                    self._menu_monedas()
                case "5":
                    self._menu_cotizaciones()
                case "6":
                    self._menu_precios()
                case "7":
                    self._menu_stock()
                case "8":
                    self._menu_reportes()
                case "0" | "salir" | "exit" | "q":
                    print("\n👋 ¡Gracias por utilizar Book Manager! Hasta luego.\n")
                    break
                case _:
                    print("⚠️ Opción no válida. Por favor, ingrese un número del menú.")

    def _menu_libros(self) -> None:
        while True:
            self.imprimir_encabezado("GESTIÓN DE LIBROS")
            print("1. Listar catálogo de libros")
            print("2. Registrar nuevo libro")
            print("3. Modificar libro existente")
            print("4. Eliminar libro")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione una acción: ").strip()

            match op:
                case "1":
                    self.listar_libros()
                case "2":
                    isbn = input("ISBN: ").strip()
                    titulo = input("Título: ").strip()
                    autor = input("Autor: ").strip()
                    id_gen = int(input("ID Género: ").strip() or "1")
                    id_ed = int(input("ID Editorial: ").strip() or "1")
                    anio_str = input("Año de publicación (Enter para omitir): ").strip()
                    paginas_str = input("Páginas (Enter para omitir): ").strip()
                    anio = int(anio_str) if anio_str else None
                    paginas = int(paginas_str) if paginas_str else None
                    self.crear_libro(isbn, titulo, autor, id_gen, id_ed, anio, paginas)
                case "3":
                    id_l = int(input("ID del libro a modificar: ").strip())
                    isbn = input("Nuevo ISBN: ").strip()
                    titulo = input("Nuevo Título: ").strip()
                    autor = input("Nuevo Autor: ").strip()
                    id_gen = int(input("Nuevo ID Género: ").strip() or "1")
                    id_ed = int(input("Nuevo ID Editorial: ").strip() or "1")
                    anio_str = input("Nuevo Año (Enter para omitir): ").strip()
                    paginas_str = input("Nuevas Páginas (Enter para omitir): ").strip()
                    anio = int(anio_str) if anio_str else None
                    paginas = int(paginas_str) if paginas_str else None
                    self.actualizar_libro(id_l, isbn, titulo, autor, id_gen, id_ed, anio, paginas)
                case "4":
                    id_l = int(input("ID del libro a eliminar: ").strip())
                    self.eliminar_libro(id_l)
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")

    def _menu_generos(self) -> None:
        while True:
            self.imprimir_encabezado("GESTIÓN DE GÉNEROS")
            print("1. Listar géneros")
            print("2. Crear nuevo género")
            print("3. Modificar género existente")
            print("4. Eliminar género")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione una acción: ").strip()
            match op:
                case "1":
                    self.listar_generos()
                case "2":
                    nom = input("Nombre del género: ").strip()
                    desc = input("Descripción: ").strip()
                    self.crear_genero(nom, desc)
                case "3":
                    id_g = int(input("ID del género a modificar: ").strip())
                    nom = input("Nuevo nombre del género: ").strip()
                    desc = input("Nueva descripción: ").strip()
                    self.actualizar_genero(id_g, nom, desc)
                case "4":
                    id_g = int(input("ID del género a eliminar: ").strip())
                    self.eliminar_genero(id_g)
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")

    def _menu_editoriales(self) -> None:
        while True:
            self.imprimir_encabezado("GESTIÓN DE EDITORIALES")
            print("1. Listar editoriales")
            print("2. Crear nueva editorial")
            print("3. Modificar editorial existente")
            print("4. Eliminar editorial")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione una acción: ").strip()
            match op:
                case "1":
                    self.listar_editoriales()
                case "2":
                    nom = input("Nombre de la editorial: ").strip()
                    pais = input("País: ").strip() or "Argentina"
                    contacto = input("Contacto: ").strip()
                    self.crear_editorial(nom, pais, contacto)
                case "3":
                    id_ed = int(input("ID de la editorial a modificar: ").strip())
                    nom = input("Nuevo nombre de la editorial: ").strip()
                    pais = input("Nuevo país: ").strip() or "Argentina"
                    contacto = input("Nuevo contacto: ").strip()
                    self.actualizar_editorial(id_ed, nom, pais, contacto)
                case "4":
                    id_ed = int(input("ID de la editorial a eliminar: ").strip())
                    self.eliminar_editorial(id_ed)
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")

    def _menu_monedas(self) -> None:
        while True:
            self.imprimir_encabezado("GESTIÓN DE MONEDAS")
            print("1. Listar monedas")
            print("2. Crear nueva moneda")
            print("3. Modificar moneda existente")
            print("4. Eliminar moneda")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione una acción: ").strip()
            match op:
                case "1":
                    self.listar_monedas()
                case "2":
                    cod = input("Código (ej. EUR): ").strip()
                    nom = input("Nombre: ").strip()
                    sim = input("Símbolo (ej. €): ").strip() or "$"
                    self.crear_moneda(cod, nom, sim)
                case "3":
                    id_m = int(input("ID de la moneda a modificar: ").strip())
                    cod = input("Nuevo código: ").strip()
                    nom = input("Nuevo nombre: ").strip()
                    sim = input("Nuevo símbolo: ").strip() or "$"
                    self.actualizar_moneda(id_m, cod, nom, sim)
                case "4":
                    id_m = int(input("ID de la moneda a eliminar: ").strip())
                    self.eliminar_moneda(id_m)
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")

    def _menu_cotizaciones(self) -> None:
        while True:
            self.imprimir_encabezado("GESTIÓN DE COTIZACIONES DE DÓLAR")
            print("1. Listar tipos de cotización")
            print("2. Crear nuevo tipo de cotización")
            print("3. Modificar tipo de cotización")
            print("4. Eliminar tipo de cotización")
            print("5. Listar histórico de cotizaciones")
            print("6. Registrar nueva cotización diaria")
            print("7. Eliminar cotización (por Tipo y Fecha)")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione una acción: ").strip()
            match op:
                case "1":
                    self.listar_tipos_cotizacion()
                case "2":
                    nom = input("Nombre del tipo de cotización: ").strip()
                    desc = input("Descripción: ").strip()
                    self.crear_tipo_cotizacion(nom, desc)
                case "3":
                    id_t = int(input("ID del tipo de cotización a modificar: ").strip())
                    nom = input("Nuevo nombre: ").strip()
                    desc = input("Nueva descripción: ").strip()
                    self.actualizar_tipo_cotizacion(id_t, nom, desc)
                case "4":
                    id_t = int(input("ID del tipo de cotización a eliminar: ").strip())
                    self.eliminar_tipo_cotizacion(id_t)
                case "5":
                    self.listar_cotizaciones()
                case "6":
                    tipo_id = int(input("ID Tipo de cotización (1=Oficial, 2=Blue, 3=MEP...): ").strip())
                    fecha = input("Fecha (YYYY-MM-DD): ").strip()
                    compra = float(input("Valor Compra ($): ").strip())
                    venta = float(input("Valor Venta ($): ").strip())
                    self.registrar_cotizacion(tipo_id, fecha, compra, venta)
                case "7":
                    tipo_id = int(input("ID Tipo de cotización: ").strip())
                    fecha = input("Fecha de cotización a eliminar (YYYY-MM-DD): ").strip()
                    self.eliminar_cotizacion(tipo_id, fecha)
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")

    def _menu_precios(self) -> None:
        while True:
            self.imprimir_encabezado("GESTIÓN DE PRECIOS")
            print("1. Listar precios")
            print("2. Fijar / Actualizar precio de libro")
            print("3. Eliminar precio")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione una acción: ").strip()
            match op:
                case "1":
                    self.listar_precios()
                case "2":
                    id_l = int(input("ID Libro: ").strip())
                    id_m = int(input("ID Moneda (1=ARS, 2=USD...): ").strip())
                    val = float(input("Valor: ").strip())
                    self.fijar_precio(id_l, id_m, val)
                case "3":
                    id_l = int(input("ID Libro: ").strip())
                    id_m = int(input("ID Moneda: ").strip())
                    self.eliminar_precio(id_l, id_m)
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")

    def _menu_stock(self) -> None:
        while True:
            self.imprimir_encabezado("GESTIÓN DE STOCK")
            print("1. Listar inventario de stock")
            print("2. Asignar / Establecer stock inicial")
            print("3. Incrementar stock (+)")
            print("4. Decrementar stock (-)")
            print("5. Eliminar registro de stock")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione una acción: ").strip()
            match op:
                case "1":
                    self.listar_stock()
                case "2":
                    id_l = int(input("ID Libro: ").strip())
                    cant = int(input("Cantidad de ejemplares: ").strip())
                    ub = input("Ubicación (Depósito Central, Sucursal Florida...): ").strip() or "Depósito Central"
                    self.asignar_stock(id_l, cant, ub)
                case "3":
                    id_l = int(input("ID Libro: ").strip())
                    cant = int(input("Cantidad a incrementar: ").strip())
                    self.incrementar_stock(id_l, cant)
                case "4":
                    id_l = int(input("ID Libro: ").strip())
                    cant = int(input("Cantidad a decrementar: ").strip())
                    self.decrementar_stock(id_l, cant)
                case "5":
                    id_l = int(input("ID Libro cuyo stock desea eliminar: ").strip())
                    self.eliminar_stock(id_l)
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")

    def _menu_reportes(self) -> None:
        while True:
            self.imprimir_encabezado("REPORTES DEL SISTEMA")
            print("1. 📖 Reporte: Catálogo Completo y Conversión Multimoneda")
            print("2. 💵 Reporte: Valorización Global del Inventario")
            print("3. ⚠️  Reporte: Alertas de Stock Crítico")
            print("4. 📊 Reporte: Distribución de Títulos por Género")
            print("0. Volver al menú principal")
            self.imprimir_separador()
            op = input("Seleccione un reporte: ").strip()
            match op:
                case "1":
                    tipo = input("Tipo de dólar para cotizar [Blue/Oficial/MEP] (def: Blue): ").strip() or "Blue"
                    self.mostrar_reporte_catalogo(tipo_dolar=tipo)
                case "2":
                    tipo = input("Tipo de dólar para cotizar [Blue/Oficial/MEP] (def: Blue): ").strip() or "Blue"
                    self.mostrar_reporte_valorizacion(tipo_dolar=tipo)
                case "3":
                    u = input("Umbral de stock crítico (def: 5): ").strip()
                    umbral = int(u) if u.isdigit() else 5
                    self.mostrar_reporte_stock_critico(umbral=umbral)
                case "4":
                    self.mostrar_reporte_generos()
                case "0":
                    break
                case _:
                    print("⚠️ Opción inválida.")
