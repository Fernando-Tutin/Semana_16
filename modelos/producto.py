"""Modelo Producto"""


class Producto:
    def __init__(self, codigo, nombre, precio, stock=0):
        self._codigo = None
        self._nombre = None
        self._precio = None
        self._stock = None

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El código no puede estar vacío.")
        self._codigo = valor.strip().upper()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser numérico.")
        if valor < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = round(valor, 2)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("El stock debe ser entero.")
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = valor

    def a_dict(self):
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "precio": self._precio,
            "stock": self._stock,
        }

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            precio=datos["precio"],
            stock=datos.get("stock", 0),
        )

    def __str__(self):
        return f"Producto({self._codigo}, {self._nombre}, ${self._precio})"
