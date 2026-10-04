"""
Modelo Usuario — Semana 16
Atributo rol incorporado: Administrador, Empleado, Cliente
"""

ROLES_VALIDOS = ("Administrador", "Empleado", "Cliente")


class Usuario:
    def __init__(self, identificador, nombre, usuario, contrasena, rol="Cliente"):
        self._identificador = None
        self._nombre = None
        self._usuario = None
        self._contrasena = None
        self._rol = None

        self.identificador = identificador
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    # ── identificador ──────────────────────────────────────────────────────
    @property
    def identificador(self):
        return self._identificador

    @identificador.setter
    def identificador(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El identificador debe ser un entero positivo.")
        self._identificador = valor

    # ── nombre ─────────────────────────────────────────────────────────────
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    # ── usuario ────────────────────────────────────────────────────────────
    @property
    def usuario(self):
        return self._usuario

    @usuario.setter
    def usuario(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre de usuario no puede estar vacío.")
        self._usuario = valor.strip()

    # ── contrasena ─────────────────────────────────────────────────────────
    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, valor):
        if not valor or len(valor.strip()) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")
        self._contrasena = valor.strip()

    # ── rol ────────────────────────────────────────────────────────────────
    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        if valor not in ROLES_VALIDOS:
            raise ValueError(f"Rol inválido. Use uno de: {ROLES_VALIDOS}")
        self._rol = valor

    # ── serialización ──────────────────────────────────────────────────────
    def a_dict(self):
        return {
            "identificador": self._identificador,
            "nombre": self._nombre,
            "usuario": self._usuario,
            "contrasena": self._contrasena,
            "rol": self._rol,
        }

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            identificador=datos["identificador"],
            nombre=datos["nombre"],
            usuario=datos["usuario"],
            contrasena=datos["contrasena"],
            rol=datos.get("rol", "Cliente"),
        )

    def __str__(self):
        return f"Usuario({self._identificador}, {self._nombre}, {self._rol})"
