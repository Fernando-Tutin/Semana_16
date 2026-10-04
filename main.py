"""
main.py — Punto de entrada de restaurante_app
Semana 16: Manejo de eventos en Tkinter
"""
import tkinter as tk
import os
import sys

# Asegurar que los módulos del proyecto sean importables
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("El Buen Sabor — Gestión de Restaurante")
        self.geometry("960x620")
        self.minsize(860, 560)
        self.configure(bg="#1E3A5F")
        self._centrar_ventana()
        self._cargar_icono()

        ruta_datos = os.path.join(os.path.dirname(__file__), "datos")
        self._servicio = RestauranteServicio(ruta_datos)
        self._usuario_activo = None
        self._vista_actual = None

        self._mostrar_login()

    def _centrar_ventana(self):
        self.update_idletasks()
        ancho = 960
        alto  = 620
        x = (self.winfo_screenwidth()  - ancho) // 2
        y = (self.winfo_screenheight() - alto)  // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _cargar_icono(self):
        try:
            from PIL import Image, ImageTk
            ruta = os.path.join(os.path.dirname(__file__),
                                "assets", "logo.png")
            img = Image.open(ruta).resize((32, 32))
            self._icono = ImageTk.PhotoImage(img)
            self.iconphoto(True, self._icono)
        except Exception:
            pass

    # ── navegación entre vistas ────────────────────────────────────────────
    def _limpiar_vista(self):
        if self._vista_actual:
            self._vista_actual.destroy()
            self._vista_actual = None

    def _mostrar_login(self):
        self._limpiar_vista()
        self._usuario_activo = None
        self._vista_actual = LoginView(
            self,
            self._servicio,
            self._al_autenticar
        )

    def _al_autenticar(self, usuario):
        self._usuario_activo = usuario
        self._limpiar_vista()
        self._vista_actual = MainView(
            self,
            self._servicio,
            self._usuario_activo,
            self._mostrar_login
        )

    def _al_cerrar_sesion(self):
        self._mostrar_login()


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
