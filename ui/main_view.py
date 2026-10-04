"""
MainView — Semana 16
Evolución: sección Usuarios con gestión completa (CRUD) y manejo de eventos:
  <<TreeviewSelect>> → cargar usuario en formulario
  <Return>           → registrar usuario
  <Escape>           → limpiar formulario y selección
  <<ComboboxSelected>> → responder al cambio de rol
  command=           → botones Registrar / Actualizar / Eliminar / Limpiar
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os

from modelos.usuario import ROLES_VALIDOS

# Paleta de colores del sistema
COLOR_FONDO        = "#F4F6FB"
COLOR_SIDEBAR      = "#1E3A5F"
COLOR_SIDEBAR_SEL  = "#2E5080"
COLOR_ACENTO       = "#2E6DA4"
COLOR_ENCABEZADO   = "#1E3A5F"
COLOR_TEXTO        = "#1A1A2E"
COLOR_ADVERTENCIA  = "#E67E22"
COLOR_PELIGRO      = "#C0392B"
COLOR_EXITO        = "#27AE60"
COLOR_FILA_PAR     = "#EAF1FB"
COLOR_FILA_IMPAR   = "#FFFFFF"


class MainView(tk.Frame):
    def __init__(self, master, servicio, usuario_activo, al_cerrar_sesion):
        super().__init__(master, bg=COLOR_FONDO)
        self._servicio      = servicio
        self._usuario_activo = usuario_activo
        self._al_cerrar_sesion = al_cerrar_sesion
        self._seccion_actual = None
        self._marcos_seccion = {}
        self._construir_ui()

    # ══════════════════════════════════════════════════════════════════════
    # CONSTRUCCIÓN GENERAL
    # ══════════════════════════════════════════════════════════════════════
    def _construir_ui(self):
        self.pack(fill="both", expand=True)
        self._construir_sidebar()
        self._construir_area_contenido()
        self._navegar("inicio")

    def _construir_sidebar(self):
        sidebar = tk.Frame(self, bg=COLOR_SIDEBAR, width=190)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo en sidebar
        ruta_logo = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
        try:
            from PIL import Image, ImageTk
            img = Image.open(ruta_logo).resize((160, 50))
            self._logo_side = ImageTk.PhotoImage(img)
            tk.Label(sidebar, image=self._logo_side,
                     bg=COLOR_SIDEBAR).pack(pady=(16, 4))
        except Exception:
            tk.Label(sidebar, text="🍽 El Buen Sabor",
                     font=("Segoe UI", 11, "bold"),
                     fg="white", bg=COLOR_SIDEBAR).pack(pady=(16, 4))

        tk.Label(sidebar, text=f"👤 {self._usuario_activo.nombre}",
                 font=("Segoe UI", 9), fg="#A0C8FF",
                 bg=COLOR_SIDEBAR).pack(pady=(0, 2))
        tk.Label(sidebar, text=self._usuario_activo.rol,
                 font=("Segoe UI", 8, "italic"), fg="#7FB3D3",
                 bg=COLOR_SIDEBAR).pack(pady=(0, 12))

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=12)

        # Botones de navegación
        secciones = [
            ("🏠  Inicio",    "inicio"),
            ("🍽  Productos", "productos"),
            ("💳  Ventas",    "ventas"),
        ]
        # Solo el Administrador ve Usuarios
        if self._usuario_activo.rol == "Administrador":
            secciones.insert(2, ("👥  Usuarios", "usuarios"))

        self._botones_nav = {}
        for texto, clave in secciones:
            btn = tk.Button(
                sidebar, text=texto, anchor="w",
                font=("Segoe UI", 10), fg="white",
                bg=COLOR_SIDEBAR, activebackground=COLOR_SIDEBAR_SEL,
                activeforeground="white", relief="flat",
                padx=16, pady=10, cursor="hand2",
                command=lambda c=clave: self._navegar(c)
            )
            btn.pack(fill="x")
            self._botones_nav[clave] = btn

        # Botón cerrar sesión al fondo
        tk.Frame(sidebar, bg=COLOR_SIDEBAR).pack(fill="y", expand=True)
        tk.Button(
            sidebar, text="🚪  Cerrar sesión",
            font=("Segoe UI", 9), fg="#FF8080",
            bg=COLOR_SIDEBAR, activebackground=COLOR_SIDEBAR_SEL,
            relief="flat", padx=16, pady=8, cursor="hand2",
            command=self._cerrar_sesion
        ).pack(fill="x", pady=(0, 8))

    def _construir_area_contenido(self):
        self._contenedor = tk.Frame(self, bg=COLOR_FONDO)
        self._contenedor.pack(side="left", fill="both", expand=True)

        # Encabezado
        self._encabezado = tk.Frame(self._contenedor,
                                    bg=COLOR_ENCABEZADO, height=50)
        self._encabezado.pack(fill="x")
        self._encabezado.pack_propagate(False)
        self._lbl_titulo = tk.Label(
            self._encabezado, text="",
            font=("Segoe UI", 14, "bold"),
            fg="white", bg=COLOR_ENCABEZADO)
        self._lbl_titulo.pack(side="left", padx=20, pady=10)

        # Área scrollable
        self._area = tk.Frame(self._contenedor, bg=COLOR_FONDO)
        self._area.pack(fill="both", expand=True, padx=20, pady=16)

    def _navegar(self, clave):
        # Resaltar botón activo
        for c, btn in self._botones_nav.items():
            btn.config(bg=COLOR_SIDEBAR_SEL if c == clave else COLOR_SIDEBAR)

        # Destruir contenido anterior
        for widget in self._area.winfo_children():
            widget.destroy()

        titulos = {
            "inicio":    "🏠  Inicio",
            "usuarios":  "👥  Gestión de Usuarios",
            "productos": "🍽  Gestión de Productos",
            "ventas":    "💳  Registro de Ventas",
        }
        self._lbl_titulo.config(text=titulos.get(clave, ""))
        self._seccion_actual = clave

        metodos = {
            "inicio":    self._construir_inicio,
            "usuarios":  self._construir_usuarios,
            "productos": self._construir_productos,
            "ventas":    self._construir_ventas,
        }
        metodos[clave]()

    # ══════════════════════════════════════════════════════════════════════
    # INICIO
    # ══════════════════════════════════════════════════════════════════════
    def _construir_inicio(self):
        tk.Label(self._area,
                 text=f"Bienvenido, {self._usuario_activo.nombre}",
                 font=("Segoe UI", 16, "bold"),
                 fg=COLOR_ACENTO, bg=COLOR_FONDO).pack(pady=(30, 8))
        tk.Label(self._area,
                 text=f"Rol: {self._usuario_activo.rol}  ·  "
                      f"Usuarios: {len(self._servicio.listar_usuarios())}  ·  "
                      f"Productos: {len(self._servicio.listar_productos())}  ·  "
                      f"Ventas: {len(self._servicio.listar_ventas())}",
                 font=("Segoe UI", 10), fg="#555", bg=COLOR_FONDO).pack()

    # ══════════════════════════════════════════════════════════════════════
    # USUARIOS  ←  NOVEDAD SEMANA 16
    # ══════════════════════════════════════════════════════════════════════
    def _construir_usuarios(self):
        """
        Sección de gestión de usuarios con CRUD completo.
        Eventos implementados:
          <<TreeviewSelect>>   → al_seleccionar_usuario
          <Return>             → al_presionar_enter  →  registrar_usuario
          <Escape>             → al_presionar_escape → limpiar_formulario
          <<ComboboxSelected>> → al_seleccionar_rol
          command=             → botones Registrar / Actualizar / Eliminar / Limpiar
        """
        # ── Aviso de sección restringida ───────────────────────────────────
        banner = tk.Frame(self._area, bg="#FFF3CD", pady=6)
        banner.pack(fill="x", pady=(0, 12))
        tk.Label(banner,
                 text="⚠  Solo el Administrador puede gestionar usuarios "
                      "(Empleado y Cliente).",
                 font=("Segoe UI", 9, "italic"),
                 fg="#856404", bg="#FFF3CD").pack(padx=12)

        # ── Layout: formulario izquierda | tabla derecha ───────────────────
        contenedor = tk.Frame(self._area, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True)

        # ─── Formulario ────────────────────────────────────────────────────
        marco_form = tk.LabelFrame(
            contenedor, text=" Datos del usuario ",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_ACENTO, bg=COLOR_FONDO, padx=14, pady=12)
        marco_form.pack(side="left", fill="y", padx=(0, 14))

        campos = [
            ("ID (auto):", None),
            ("Nombre completo *:", None),
            ("Nombre de usuario *:", None),
            ("Contraseña *:", None),
            ("Rol *:", None),
        ]
        self._u_id_var         = tk.StringVar()
        self._u_nombre_var     = tk.StringVar()
        self._u_usuario_var    = tk.StringVar()
        self._u_contrasena_var = tk.StringVar()
        self._u_rol_var        = tk.StringVar(value="Empleado")

        variables = [
            self._u_id_var,
            self._u_nombre_var,
            self._u_usuario_var,
            self._u_contrasena_var,
            self._u_rol_var,
        ]

        for i, ((etiqueta, _), var) in enumerate(zip(campos, variables)):
            tk.Label(marco_form, text=etiqueta, font=("Segoe UI", 10),
                     bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(
                row=i, column=0, sticky="w", pady=5)

            if etiqueta.startswith("Rol"):
                # Combobox para seleccionar rol
                self._combo_rol = ttk.Combobox(
                    marco_form, textvariable=var,
                    values=["Empleado", "Cliente"],
                    state="readonly", width=20, font=("Segoe UI", 10))
                self._combo_rol.grid(row=i, column=1, pady=5, sticky="w")
                # ── <<ComboboxSelected>> ──────────────────────────────────
                self._combo_rol.bind(
                    "<<ComboboxSelected>>", self._al_seleccionar_rol)
            elif etiqueta.startswith("Contraseña"):
                entry = ttk.Entry(marco_form, textvariable=var,
                                  width=22, show="*", font=("Segoe UI", 10))
                entry.grid(row=i, column=1, pady=5, sticky="w")
                self._u_contrasena_entry = entry
            elif etiqueta.startswith("ID"):
                entry = ttk.Entry(marco_form, textvariable=var,
                                  width=22, state="disabled",
                                  font=("Segoe UI", 10))
                entry.grid(row=i, column=1, pady=5, sticky="w")
            else:
                entry = ttk.Entry(marco_form, textvariable=var,
                                  width=22, font=("Segoe UI", 10))
                entry.grid(row=i, column=1, pady=5, sticky="w")
                if etiqueta.startswith("Nombre completo"):
                    self._u_nombre_entry = entry
                elif etiqueta.startswith("Nombre de usuario"):
                    self._u_usuario_entry = entry

        # Info de rol seleccionado
        self._lbl_info_rol = tk.Label(
            marco_form, text="ℹ  Rol seleccionado: Empleado",
            font=("Segoe UI", 8, "italic"), fg="#555", bg=COLOR_FONDO)
        self._lbl_info_rol.grid(row=5, column=0, columnspan=2,
                                sticky="w", pady=(0, 8))

        # Nota de contraseña en edición
        tk.Label(marco_form,
                 text="* En actualizar: dejar contraseña\n  vacía para no cambiarla.",
                 font=("Segoe UI", 8, "italic"),
                 fg=COLOR_ADVERTENCIA, bg=COLOR_FONDO).grid(
            row=6, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # ── Botones (command=) ─────────────────────────────────────────────
        marco_btn = tk.Frame(marco_form, bg=COLOR_FONDO)
        marco_btn.grid(row=7, column=0, columnspan=2, pady=(6, 0))

        ttk.Button(marco_btn, text="✔ Registrar",
                   command=self._registrar_usuario).grid(
            row=0, column=0, padx=4, pady=3, sticky="ew")
        ttk.Button(marco_btn, text="✏ Actualizar",
                   command=self._actualizar_usuario).grid(
            row=0, column=1, padx=4, pady=3, sticky="ew")
        ttk.Button(marco_btn, text="🗑 Eliminar",
                   command=self._eliminar_usuario).grid(
            row=1, column=0, padx=4, pady=3, sticky="ew")
        ttk.Button(marco_btn, text="⟳ Limpiar",
                   command=self._limpiar_formulario_usuario).grid(
            row=1, column=1, padx=4, pady=3, sticky="ew")

        tk.Label(marco_form,
                 text="Atajos:  Enter → Registrar  |  Esc → Limpiar",
                 font=("Segoe UI", 8, "italic"), fg="#888",
                 bg=COLOR_FONDO).grid(row=8, column=0, columnspan=2, pady=(6, 0))

        # ── Bindings de teclado ────────────────────────────────────────────
        # <Return> en cualquier Entry del formulario → registrar
        for entry_widget in (
            self._u_nombre_entry,
            self._u_usuario_entry,
            self._u_contrasena_entry,
        ):
            entry_widget.bind("<Return>", self._al_presionar_enter)
            entry_widget.bind("<Escape>", self._al_presionar_escape)

        # ─── Tabla Treeview ────────────────────────────────────────────────
        marco_tabla = tk.LabelFrame(
            contenedor, text=" Usuarios registrados ",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_ACENTO, bg=COLOR_FONDO)
        marco_tabla.pack(side="left", fill="both", expand=True)

        columnas = ("ID", "Nombre", "Usuario", "Rol")
        self._tabla_usuarios = ttk.Treeview(
            marco_tabla, columns=columnas,
            show="headings", height=16)

        anchos = {"ID": 50, "Nombre": 160, "Usuario": 120, "Rol": 100}
        for col in columnas:
            self._tabla_usuarios.heading(col, text=col)
            self._tabla_usuarios.column(col, width=anchos[col], anchor="center")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical",
                               command=self._tabla_usuarios.yview)
        self._tabla_usuarios.configure(yscrollcommand=scroll.set)
        self._tabla_usuarios.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._tabla_usuarios.tag_configure("par",   background=COLOR_FILA_PAR)
        self._tabla_usuarios.tag_configure("impar", background=COLOR_FILA_IMPAR)

        # ── <<TreeviewSelect>> ─────────────────────────────────────────────
        self._tabla_usuarios.bind(
            "<<TreeviewSelect>>", self._al_seleccionar_usuario)

        self._actualizar_tabla_usuarios()

    # ── Callbacks de eventos — Usuarios ────────────────────────────────────
    def _al_seleccionar_usuario(self, event):
        """
        <<TreeviewSelect>> → obtiene identificador de la fila
        → consulta el objeto Usuario en el servicio
        → carga los datos en el formulario.
        La contraseña NO se muestra por seguridad.
        """
        seleccion = self._tabla_usuarios.selection()
        if not seleccion:
            return
        valores = self._tabla_usuarios.item(seleccion[0], "values")
        usuario = self._servicio.buscar_usuario(valores[0])
        if usuario is None:
            return
        self._cargar_usuario_en_formulario(usuario)

    def _al_presionar_enter(self, event):
        """<Return> en el formulario → reutiliza registrar_usuario."""
        self._registrar_usuario()

    def _al_presionar_escape(self, event):
        """<Escape> → limpia formulario y cancela selección."""
        self._limpiar_formulario_usuario()

    def _al_seleccionar_rol(self, event):
        """<<ComboboxSelected>> → actualiza la etiqueta informativa del rol."""
        rol = self._u_rol_var.get()
        descripciones = {
            "Empleado": "Accede a Productos y Ventas.",
            "Cliente":  "Acceso básico al sistema.",
        }
        self._lbl_info_rol.config(
            text=f"ℹ  Rol seleccionado: {rol} — {descripciones.get(rol, '')}")

    # ── Acciones CRUD — Usuarios ───────────────────────────────────────────
    def _registrar_usuario(self):
        nombre     = self._u_nombre_var.get().strip()
        usuario_s  = self._u_usuario_var.get().strip()
        contrasena = self._u_contrasena_var.get().strip()
        rol        = self._u_rol_var.get()
        try:
            self._servicio.registrar_usuario(nombre, usuario_s, contrasena, rol)
            self._actualizar_tabla_usuarios()
            self._limpiar_formulario_usuario()
            messagebox.showinfo("Registrado",
                                f"Usuario '{usuario_s}' registrado correctamente.",
                                parent=self)
        except ValueError as error:
            messagebox.showerror("Error al registrar", str(error), parent=self)

    def _actualizar_usuario(self):
        id_str     = self._u_id_var.get().strip()
        nombre     = self._u_nombre_var.get().strip()
        usuario_s  = self._u_usuario_var.get().strip()
        contrasena = self._u_contrasena_var.get().strip()
        rol        = self._u_rol_var.get()
        if not id_str:
            messagebox.showwarning("Sin selección",
                                   "Selecciona un usuario de la tabla primero.",
                                   parent=self)
            return
        try:
            self._servicio.actualizar_usuario(
                id_str, nombre, usuario_s, contrasena, rol,
                self._usuario_activo)
            self._actualizar_tabla_usuarios()
            self._limpiar_formulario_usuario()
            messagebox.showinfo("Actualizado",
                                "Usuario actualizado correctamente.",
                                parent=self)
        except ValueError as error:
            messagebox.showerror("Error al actualizar", str(error), parent=self)

    def _eliminar_usuario(self):
        id_str = self._u_id_var.get().strip()
        if not id_str:
            messagebox.showwarning("Sin selección",
                                   "Selecciona un usuario de la tabla primero.",
                                   parent=self)
            return
        usuario = self._servicio.buscar_usuario(id_str)
        if usuario is None:
            return
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Eliminar al usuario '{usuario.nombre}' ({usuario.rol})?",
            parent=self)
        if not confirmar:
            return
        try:
            self._servicio.eliminar_usuario(id_str, self._usuario_activo)
            self._actualizar_tabla_usuarios()
            self._limpiar_formulario_usuario()
            messagebox.showinfo("Eliminado",
                                "Usuario eliminado correctamente.",
                                parent=self)
        except ValueError as error:
            messagebox.showerror("Error al eliminar", str(error), parent=self)

    def _limpiar_formulario_usuario(self):
        """Limpia el formulario y cancela la selección del Treeview."""
        self._u_id_var.set("")
        self._u_nombre_var.set("")
        self._u_usuario_var.set("")
        self._u_contrasena_var.set("")
        self._u_rol_var.set("Empleado")
        self._lbl_info_rol.config(text="ℹ  Rol seleccionado: Empleado")
        # Cancelar selección en la tabla
        seleccion = self._tabla_usuarios.selection()
        if seleccion:
            self._tabla_usuarios.selection_remove(seleccion)
        self._u_nombre_entry.focus()

    def _cargar_usuario_en_formulario(self, usuario):
        """Carga un objeto Usuario en el formulario (sin exponer contraseña)."""
        self._u_id_var.set(str(usuario.identificador))
        self._u_nombre_var.set(usuario.nombre)
        self._u_usuario_var.set(usuario.usuario)
        self._u_contrasena_var.set("")     # No mostrar contraseña
        self._u_rol_var.set(usuario.rol)
        self._lbl_info_rol.config(
            text=f"ℹ  Rol seleccionado: {usuario.rol}")

    def _actualizar_tabla_usuarios(self):
        for item in self._tabla_usuarios.get_children():
            self._tabla_usuarios.delete(item)
        for i, u in enumerate(self._servicio.listar_usuarios()):
            tag = "par" if i % 2 == 0 else "impar"
            self._tabla_usuarios.insert(
                "", "end",
                values=(u.identificador, u.nombre, u.usuario, u.rol),
                tags=(tag,))

    # ══════════════════════════════════════════════════════════════════════
    # PRODUCTOS
    # ══════════════════════════════════════════════════════════════════════
    def _construir_productos(self):
        contenedor = tk.Frame(self._area, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True)

        # Formulario
        marco_form = tk.LabelFrame(
            contenedor, text=" Datos del producto ",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_ACENTO, bg=COLOR_FONDO, padx=14, pady=12)
        marco_form.pack(side="left", fill="y", padx=(0, 14))

        self._p_codigo_var = tk.StringVar()
        self._p_nombre_var = tk.StringVar()
        self._p_precio_var = tk.StringVar()
        self._p_stock_var  = tk.StringVar()

        for i, (etiqueta, var) in enumerate([
            ("Código *:",  self._p_codigo_var),
            ("Nombre *:",  self._p_nombre_var),
            ("Precio *:",  self._p_precio_var),
            ("Stock:",     self._p_stock_var),
        ]):
            tk.Label(marco_form, text=etiqueta, font=("Segoe UI", 10),
                     bg=COLOR_FONDO).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Entry(marco_form, textvariable=var,
                      width=22, font=("Segoe UI", 10)).grid(
                row=i, column=1, pady=5, sticky="w")

        marco_btn = tk.Frame(marco_form, bg=COLOR_FONDO)
        marco_btn.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        ttk.Button(marco_btn, text="✔ Registrar",
                   command=self._registrar_producto).grid(row=0, column=0, padx=4)
        ttk.Button(marco_btn, text="✏ Actualizar",
                   command=self._actualizar_producto).grid(row=0, column=1, padx=4)
        ttk.Button(marco_btn, text="🗑 Eliminar",
                   command=self._eliminar_producto).grid(row=1, column=0, padx=4, pady=3)
        ttk.Button(marco_btn, text="⟳ Limpiar",
                   command=self._limpiar_producto).grid(row=1, column=1, padx=4, pady=3)

        # Tabla
        marco_tabla = tk.LabelFrame(
            contenedor, text=" Productos ",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_ACENTO, bg=COLOR_FONDO)
        marco_tabla.pack(side="left", fill="both", expand=True)

        columnas = ("Código", "Nombre", "Precio", "Stock")
        self._tabla_productos = ttk.Treeview(
            marco_tabla, columns=columnas, show="headings", height=16)
        for col in columnas:
            self._tabla_productos.heading(col, text=col)
            self._tabla_productos.column(col, width=120, anchor="center")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical",
                               command=self._tabla_productos.yview)
        self._tabla_productos.configure(yscrollcommand=scroll.set)
        self._tabla_productos.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._tabla_productos.tag_configure("par",   background=COLOR_FILA_PAR)
        self._tabla_productos.tag_configure("impar", background=COLOR_FILA_IMPAR)
        self._tabla_productos.bind("<<TreeviewSelect>>",
                                   self._al_seleccionar_producto)
        self._refrescar_productos()

    def _al_seleccionar_producto(self, event):
        seleccion = self._tabla_productos.selection()
        if not seleccion:
            return
        valores = self._tabla_productos.item(seleccion[0], "values")
        producto = self._servicio.buscar_producto(valores[0])
        if producto is None:
            return
        self._p_codigo_var.set(producto.codigo)
        self._p_nombre_var.set(producto.nombre)
        self._p_precio_var.set(str(producto.precio))
        self._p_stock_var.set(str(producto.stock))

    def _registrar_producto(self):
        try:
            self._servicio.registrar_producto(
                self._p_codigo_var.get(),
                self._p_nombre_var.get(),
                self._p_precio_var.get(),
                self._p_stock_var.get() or 0)
            self._refrescar_productos()
            self._limpiar_producto()
            messagebox.showinfo("Registrado", "Producto registrado.", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _actualizar_producto(self):
        codigo = self._p_codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Sin selección",
                                   "Selecciona un producto primero.", parent=self)
            return
        try:
            self._servicio.actualizar_producto(
                codigo,
                self._p_nombre_var.get(),
                self._p_precio_var.get(),
                self._p_stock_var.get() or 0)
            self._refrescar_productos()
            self._limpiar_producto()
            messagebox.showinfo("Actualizado", "Producto actualizado.", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _eliminar_producto(self):
        codigo = self._p_codigo_var.get().strip()
        if not codigo:
            messagebox.showwarning("Sin selección",
                                   "Selecciona un producto primero.", parent=self)
            return
        if not messagebox.askyesno("Confirmar",
                                   f"¿Eliminar producto '{codigo}'?",
                                   parent=self):
            return
        try:
            self._servicio.eliminar_producto(codigo)
            self._refrescar_productos()
            self._limpiar_producto()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _limpiar_producto(self):
        for var in (self._p_codigo_var, self._p_nombre_var,
                    self._p_precio_var, self._p_stock_var):
            var.set("")
        sel = self._tabla_productos.selection()
        if sel:
            self._tabla_productos.selection_remove(sel)

    def _refrescar_productos(self):
        for item in self._tabla_productos.get_children():
            self._tabla_productos.delete(item)
        for i, p in enumerate(self._servicio.listar_productos()):
            tag = "par" if i % 2 == 0 else "impar"
            self._tabla_productos.insert(
                "", "end",
                values=(p.codigo, p.nombre, f"${p.precio:.2f}", p.stock),
                tags=(tag,))

    # ══════════════════════════════════════════════════════════════════════
    # VENTAS
    # ══════════════════════════════════════════════════════════════════════
    def _construir_ventas(self):
        marco_form = tk.LabelFrame(
            self._area, text=" Registrar venta ",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_ACENTO, bg=COLOR_FONDO, padx=14, pady=12)
        marco_form.pack(fill="x", pady=(0, 16))

        tk.Label(marco_form, text="Usuario:", font=("Segoe UI", 10),
                 bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", pady=5)
        self._v_usuario_var = tk.StringVar()
        opciones_u = [f"{u.identificador} – {u.nombre}"
                      for u in self._servicio.listar_usuarios()]
        self._combo_u_venta = ttk.Combobox(
            marco_form, textvariable=self._v_usuario_var,
            values=opciones_u, state="readonly", width=28)
        self._combo_u_venta.grid(row=0, column=1, pady=5, padx=8)

        tk.Label(marco_form, text="Producto:", font=("Segoe UI", 10),
                 bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", pady=5)
        self._v_producto_var = tk.StringVar()
        opciones_p = [f"{p.codigo} – {p.nombre} (stock:{p.stock})"
                      for p in self._servicio.listar_productos()]
        self._combo_p_venta = ttk.Combobox(
            marco_form, textvariable=self._v_producto_var,
            values=opciones_p, state="readonly", width=28)
        self._combo_p_venta.grid(row=1, column=1, pady=5, padx=8)

        ttk.Button(marco_form, text="💳 Registrar venta",
                   command=self._registrar_venta).grid(
            row=2, column=0, columnspan=2, pady=(12, 0))

        # Tabla ventas
        marco_tabla = tk.LabelFrame(
            self._area, text=" Historial de ventas ",
            font=("Segoe UI", 10, "bold"),
            fg=COLOR_ACENTO, bg=COLOR_FONDO)
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("ID", "Usuario ID", "Producto", "Fecha")
        self._tabla_ventas = ttk.Treeview(
            marco_tabla, columns=columnas, show="headings", height=12)
        for col in columnas:
            self._tabla_ventas.heading(col, text=col)
            self._tabla_ventas.column(col, width=130, anchor="center")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical",
                               command=self._tabla_ventas.yview)
        self._tabla_ventas.configure(yscrollcommand=scroll.set)
        self._tabla_ventas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._tabla_ventas.tag_configure("par",   background=COLOR_FILA_PAR)
        self._tabla_ventas.tag_configure("impar", background=COLOR_FILA_IMPAR)
        self._refrescar_ventas()

    def _registrar_venta(self):
        u_sel = self._v_usuario_var.get()
        p_sel = self._v_producto_var.get()
        if not u_sel or not p_sel:
            messagebox.showwarning("Campos incompletos",
                                   "Selecciona usuario y producto.", parent=self)
            return
        try:
            usuario_id = int(u_sel.split(" – ")[0])
            producto_codigo = p_sel.split(" – ")[0]
            self._servicio.registrar_venta(usuario_id, producto_codigo)
            self._refrescar_ventas()
            messagebox.showinfo("Venta registrada",
                                "Venta registrada correctamente.", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _refrescar_ventas(self):
        for item in self._tabla_ventas.get_children():
            self._tabla_ventas.delete(item)
        for i, v in enumerate(self._servicio.listar_ventas()):
            tag = "par" if i % 2 == 0 else "impar"
            self._tabla_ventas.insert(
                "", "end",
                values=(v.identificador, v.usuario_id,
                        v.producto_codigo, v.fecha),
                tags=(tag,))

    # ══════════════════════════════════════════════════════════════════════
    # CIERRE DE SESIÓN
    # ══════════════════════════════════════════════════════════════════════
    def _cerrar_sesion(self):
        if messagebox.askyesno("Cerrar sesión",
                               "¿Deseas cerrar la sesión actual?",
                               parent=self):
            self._al_cerrar_sesion()
