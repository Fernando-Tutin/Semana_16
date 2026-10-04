"""
Genera íconos y logo para restaurante_app usando solo Pillow.
Ejecutar una sola vez: python assets/generar_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

DIRECTORIO = os.path.dirname(os.path.abspath(__file__))


def _crear_icono(nombre, color_fondo, texto, tam=32):
    img = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, tam - 1, tam - 1], fill=color_fondo)
    draw.text((tam // 2, tam // 2), texto, fill="white", anchor="mm")
    img.save(os.path.join(DIRECTORIO, nombre))


def _crear_logo():
    w, h = 260, 80
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Fondo redondeado
    draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=14,
                            fill=(30, 80, 160))
    # Ícono de tenedor/cuchillo
    for x in [30, 38]:
        draw.line([(x, 14), (x, 50)], fill="white", width=3)
    draw.arc([22, 14, 46, 36], start=0, end=180, fill="white", width=3)
    # Texto
    draw.text((70, h // 2), "El Buen Sabor", fill="white", anchor="lm")
    draw.text((70, h // 2 + 18), "Gestión de Restaurante", fill="#A0C8FF", anchor="lm")
    img.save(os.path.join(DIRECTORIO, "logo.png"))


if __name__ == "__main__":
    _crear_logo()
    _crear_icono("icon_inicio.png",    (30, 80, 160),  "🏠", 32)
    _crear_icono("icon_usuarios.png",  (0, 140, 90),   "👤", 32)
    _crear_icono("icon_productos.png", (180, 80, 0),   "🍽", 32)
    _crear_icono("icon_ventas.png",    (140, 0, 100),  "💳", 32)
    print("Assets generados en:", DIRECTORIO)
