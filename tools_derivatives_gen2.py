#!/usr/bin/env python3
"""Derivadas responsive para las fotografias de seccion (assets/img/xaru/gen2).

Las mismas fotos sirven de fondo de cabecera a pantalla completa y de imagen de
tarjeta a ~440 px. Servir el master de 1920 px en los dos sitios es lo que
llevaba la portada a 11,7 MB. Aqui se generan WebP y JPEG a 768/1280/1920 y el
generador elige el ancho segun el papel de cada imagen.
"""
import os, glob
from PIL import Image

WIDTHS = [768, 1280, 1920]
SRC = "assets/img/xaru/gen2"
OUT = "assets/img/xaru/gen2/r"

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    made = 0
    for p in sorted(glob.glob(SRC + "/*.jpg")):
        base = os.path.splitext(os.path.basename(p))[0]
        im = Image.open(p).convert("RGB")
        W, H = im.size
        for w in WIDTHS:
            # Si el master es mas estrecho que el ancho pedido no se inventa
            # resolucion: se escribe el master tal cual bajo ese nombre. Asi la
            # URL existe siempre y ninguna pagina se queda sin fondo por un 404.
            rs = im if w >= W else im.resize((w, round(H * w / W)), Image.LANCZOS)
            for ext, kw in (("avif", dict(quality=58)),
                            ("webp", dict(quality=78, method=6)),
                            ("jpg",  dict(quality=80, optimize=True, progressive=True))):
                out = "%s/%s-%d.%s" % (OUT, base, w, ext)
                rs.save(out, **kw)
                made += 1
    print("derivadas gen2:", made)
