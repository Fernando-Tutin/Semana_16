"""
LoginView — vista de inicio de sesión
Semana 16: sin cambios funcionales; conservada desde semanas anteriores.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os


class LoginView(tk.Frame):
    def __init__(self, master, servicio, al_autenticar):
        super().__init__(master, bg="#1E3A5F")
        self._servicio = servicio
        self._al_autenticar = al_autenticar
        self._construir_ui()

    def _construir_ui(self):
        self.pack(fill="both", expand=True)

        # Logo
        ruta_logo = os.path.join(
            os.path.dirname(__file__), "..", "assets", "logo.png"
        )
        try:
            from PIL import Image, ImageTk
            img = Image.open(ruta_logo).resize((260, 80))
            self._logo = ImageTk.PhotoImage(img)
            tk.Label(self, image=self._logo, bg="#1E3A5F").pack(pady=(40, 10))
        except Exception:
            tk.Label(self, text="🍽  El Buen Sabor",
                     font=("Segoe UI", 20, "bold"),
                     fg="white", bg="#1E3A5F").pack(pady=(40, 10))

        tk.Label(self, text="Gestión de Restaurante",
                 font=("Segoe UI", 11), fg="#A0C8FF", bg="#1E3A5F").pack()

        # Tarjeta de login
        tarjeta = tk.Frame(self, bg="white", padx=30, pady=24)
        tarjeta.pack(pady=30, ipadx=10, ipady=10)

        tk.Label(tarjeta, text="Iniciar sesión",
                 font=("Segoe UI", 14, "bold"),
                 fg="#1E3A5F", bg="white").grid(row=0, column=0, columnspan=2,
                                                 pady=(0, 16))

        tk.Label(tarjeta, text="Usuario:", font=("Segoe UI", 10),
                 bg="white").grid(row=1, column=0, sticky="w", pady=4)
        self._entrada_usuario = ttk.Entry(tarjeta, width=24,
                                           font=("Segoe UI", 10))
        self._entrada_usuario.grid(row=1, column=1, pady=4)

        tk.Label(tarjeta, text="Contraseña:", font=("Segoe UI", 10),
                 bg="white").grid(row=2, column=0, sticky="w", pady=4)
        self._entrada_contrasena = ttk.Entry(tarjeta, width=24, show="*",
                                              font=("Segoe UI", 10))
        self._entrada_contrasena.grid(row=2, column=1, pady=4)

        ttk.Button(tarjeta, text="Ingresar",
                   command=self._iniciar_sesion).grid(
            row=3, column=0, columnspan=2, pady=(16, 0), sticky="ew")

        # ── Eventos de teclado: Enter confirma, Escape limpia ──────────────
        self._entrada_usuario.bind("<Return>", self._al_presionar_enter)
        self._entrada_contrasena.bind("<Return>", self._al_presionar_enter)
        self._entrada_contrasena.bind("<Escape>", self._al_presionar_escape)

        self._entrada_usuario.focus()

    # ── callbacks ──────────────────────────────────────────────────────────
    def _al_presionar_enter(self, event):
        """<Return> confirma el login reutilizando _iniciar_sesion."""
        self._iniciar_sesion()

    def _al_presionar_escape(self, event):
        """<Escape> limpia los campos."""
        self._entrada_usuario.delete(0, tk.END)
        self._entrada_contrasena.delete(0, tk.END)
        self._entrada_usuario.focus()

    def _iniciar_sesion(self):
        usuario_str = self._entrada_usuario.get().strip()
        contrasena_str = self._entrada_contrasena.get().strip()
        if not usuario_str or not contrasena_str:
            messagebox.showwarning("Campos incompletos",
                                   "Ingresa usuario y contraseña.",
                                   parent=self)
            return
        usuario = self._servicio.validar_acceso(usuario_str, contrasena_str)
        if usuario:
            self._al_autenticar(usuario)
        else:
            messagebox.showerror("Acceso denegado",
                                 "Usuario o contraseña incorrectos.",
                                 parent=self)
            self._entrada_contrasena.delete(0, tk.END)
            self._entrada_contrasena.focus()
