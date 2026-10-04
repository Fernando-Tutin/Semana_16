"""
RestauranteServicio — Semana 16
CRUD completo para Usuario (con rol), Producto y Venta.
Toda la lógica de negocio y persistencia reside aquí.
"""
from modelos.usuario import Usuario, ROLES_VALIDOS
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    def __init__(self, ruta_datos):
        self._archivo = ArchivoServicio(ruta_datos)
        self._usuarios: list[Usuario] = []
        self._productos: list[Producto] = []
        self._ventas: list[Venta] = []
        self._cargar_todo()

    # ══════════════════════════════════════════════════════════════════════
    # INICIALIZACIÓN
    # ══════════════════════════════════════════════════════════════════════
    def _cargar_todo(self):
        for d in self._archivo.cargar_usuarios():
            self._usuarios.append(Usuario.desde_dict(d))
        for d in self._archivo.cargar_productos():
            self._productos.append(Producto.desde_dict(d))
        for d in self._archivo.cargar_ventas():
            self._ventas.append(Venta.desde_dict(d))

    # ══════════════════════════════════════════════════════════════════════
    # AUTENTICACIÓN
    # ══════════════════════════════════════════════════════════════════════
    def validar_acceso(self, usuario_str, contrasena_str):
        """Devuelve el objeto Usuario si las credenciales son correctas, None si no."""
        for u in self._usuarios:
            if u.usuario == usuario_str and u.contrasena == contrasena_str:
                return u
        return None

    # ══════════════════════════════════════════════════════════════════════
    # USUARIOS — CRUD COMPLETO  (Semana 16)
    # ══════════════════════════════════════════════════════════════════════
    def listar_usuarios(self):
        return list(self._usuarios)

    def buscar_usuario(self, identificador):
        """Devuelve el Usuario con ese identificador, o None."""
        try:
            id_int = int(identificador)
        except (TypeError, ValueError):
            return None
        for u in self._usuarios:
            if u.identificador == id_int:
                return u
        return None

    def registrar_usuario(self, nombre, usuario_str, contrasena, rol):
        """Registra un nuevo usuario. Solo Empleado y Cliente pueden crearse desde la UI."""
        if rol not in ("Empleado", "Cliente"):
            raise ValueError("Solo se pueden registrar usuarios de tipo Empleado o Cliente.")
        if self._usuario_existente(usuario_str):
            raise ValueError(f"El nombre de usuario '{usuario_str}' ya está en uso.")

        nuevo_id = self._siguiente_id_usuario()
        nuevo = Usuario(nuevo_id, nombre, usuario_str, contrasena, rol)
        self._usuarios.append(nuevo)
        self._persistir_usuarios()
        return nuevo

    def actualizar_usuario(self, identificador, nombre, usuario_str, contrasena, rol, usuario_activo):
        """
        Actualiza un usuario existente.
        - No permite cambiar el rol de un Administrador.
        - El administrador autenticado no puede degradar su propio rol.
        """
        objetivo = self.buscar_usuario(identificador)
        if objetivo is None:
            raise ValueError("Usuario no encontrado.")

        # Regla: no permitir editar otro Administrador desde la UI
        if objetivo.rol == "Administrador" and objetivo.identificador != usuario_activo.identificador:
            raise ValueError("No se puede modificar otro usuario Administrador.")

        # Regla: el admin activo no puede cambiar su propio rol
        if objetivo.identificador == usuario_activo.identificador and rol != "Administrador":
            raise ValueError("No puedes cambiar tu propio rol de Administrador.")

        if self._usuario_existente(usuario_str, excluir_id=int(identificador)):
            raise ValueError(f"El nombre de usuario '{usuario_str}' ya está en uso.")

        objetivo.nombre = nombre
        objetivo.usuario = usuario_str
        if contrasena.strip():
            objetivo.contrasena = contrasena
        objetivo.rol = rol
        self._persistir_usuarios()
        return objetivo

    def eliminar_usuario(self, identificador, usuario_activo):
        """
        Elimina un usuario.
        - No permite eliminar al administrador autenticado.
        - No permite eliminar a otro Administrador.
        """
        objetivo = self.buscar_usuario(identificador)
        if objetivo is None:
            raise ValueError("Usuario no encontrado.")
        if objetivo.identificador == usuario_activo.identificador:
            raise ValueError("No puedes eliminar tu propia cuenta.")
        if objetivo.rol == "Administrador":
            raise ValueError("No se puede eliminar otro usuario Administrador.")

        self._usuarios.remove(objetivo)
        self._persistir_usuarios()

    # ── helpers usuarios ───────────────────────────────────────────────────
    def _usuario_existente(self, usuario_str, excluir_id=None):
        for u in self._usuarios:
            if excluir_id and u.identificador == excluir_id:
                continue
            if u.usuario == usuario_str:
                return True
        return False

    def _siguiente_id_usuario(self):
        if not self._usuarios:
            return 1
        return max(u.identificador for u in self._usuarios) + 1

    def _persistir_usuarios(self):
        self._archivo.guardar_usuarios([u.a_dict() for u in self._usuarios])

    # ══════════════════════════════════════════════════════════════════════
    # PRODUCTOS — CRUD
    # ══════════════════════════════════════════════════════════════════════
    def listar_productos(self):
        return list(self._productos)

    def buscar_producto(self, codigo):
        for p in self._productos:
            if p.codigo == codigo.upper():
                return p
        return None

    def registrar_producto(self, codigo, nombre, precio, stock):
        if self.buscar_producto(codigo):
            raise ValueError(f"Ya existe un producto con código '{codigo}'.")
        nuevo = Producto(codigo, nombre, precio, stock)
        self._productos.append(nuevo)
        self._archivo.guardar_productos([p.a_dict() for p in self._productos])
        return nuevo

    def actualizar_producto(self, codigo, nombre, precio, stock):
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("Producto no encontrado.")
        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock
        self._archivo.guardar_productos([p.a_dict() for p in self._productos])
        return producto

    def eliminar_producto(self, codigo):
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError("Producto no encontrado.")
        self._productos.remove(producto)
        self._archivo.guardar_productos([p.a_dict() for p in self._productos])

    # ══════════════════════════════════════════════════════════════════════
    # VENTAS
    # ══════════════════════════════════════════════════════════════════════
    def listar_ventas(self):
        return list(self._ventas)

    def registrar_venta(self, usuario_id, producto_codigo):
        producto = self.buscar_producto(producto_codigo)
        if producto is None:
            raise ValueError("Producto no encontrado.")
        if producto.stock <= 0:
            raise ValueError("Sin stock disponible.")
        producto.stock -= 1
        identificador = self._generar_id_venta()
        nueva = Venta(identificador, usuario_id, producto_codigo)
        self._ventas.append(nueva)
        self._archivo.guardar_ventas([v.a_dict() for v in self._ventas])
        self._archivo.guardar_productos([p.a_dict() for p in self._productos])
        return nueva

    def _generar_id_venta(self):
        if not self._ventas:
            return "V001"
        ultimo = max(int(v.identificador[1:]) for v in self._ventas)
        return f"V{ultimo + 1:03d}"
