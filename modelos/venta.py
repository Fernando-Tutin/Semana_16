"""Modelo Venta"""
from datetime import date


class Venta:
    def __init__(self, identificador, usuario_id, producto_codigo, fecha=None):
        self._identificador = identificador
        self._usuario_id = usuario_id
        self._producto_codigo = producto_codigo
        self._fecha = fecha or str(date.today())

    @property
    def identificador(self):
        return self._identificador

    @property
    def usuario_id(self):
        return self._usuario_id

    @property
    def producto_codigo(self):
        return self._producto_codigo

    @property
    def fecha(self):
        return self._fecha

    def a_dict(self):
        return {
            "identificador": self._identificador,
            "usuario_id": self._usuario_id,
            "producto_codigo": self._producto_codigo,
            "fecha": self._fecha,
        }

    @classmethod
    def desde_dict(cls, datos):
        return cls(
            identificador=datos["identificador"],
            usuario_id=datos["usuario_id"],
            producto_codigo=datos["producto_codigo"],
            fecha=datos.get("fecha"),
        )

    def __str__(self):
        return f"Venta({self._identificador}, usuario={self._usuario_id}, producto={self._producto_codigo})"
