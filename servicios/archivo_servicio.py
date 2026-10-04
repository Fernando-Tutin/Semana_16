"""
ArchivoServicio — lectura y escritura de archivos JSON.
No conoce modelos; trabaja con listas de dicts.
"""
import json
import os


class ArchivoServicio:
    def __init__(self, ruta_base):
        self._ruta_base = ruta_base

    def _ruta(self, nombre_archivo):
        return os.path.join(self._ruta_base, nombre_archivo)

    # ── usuarios ───────────────────────────────────────────────────────────
    def cargar_usuarios(self):
        ruta = self._ruta("usuarios.json")
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar_usuarios(self, lista_dicts):
        with open(self._ruta("usuarios.json"), "w", encoding="utf-8") as archivo:
            json.dump(lista_dicts, archivo, ensure_ascii=False, indent=2)

    # ── productos ──────────────────────────────────────────────────────────
    def cargar_productos(self):
        ruta = self._ruta("productos.json")
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar_productos(self, lista_dicts):
        with open(self._ruta("productos.json"), "w", encoding="utf-8") as archivo:
            json.dump(lista_dicts, archivo, ensure_ascii=False, indent=2)

    # ── ventas ─────────────────────────────────────────────────────────────
    def cargar_ventas(self):
        ruta = self._ruta("ventas.json")
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def guardar_ventas(self, lista_dicts):
        with open(self._ruta("ventas.json"), "w", encoding="utf-8") as archivo:
            json.dump(lista_dicts, archivo, ensure_ascii=False, indent=2)
