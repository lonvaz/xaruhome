#!/usr/bin/env python3
"""Genera derivadas responsive (AVIF/WebP/JPEG) para el catalogo XARU HOME.
Anchos: 480, 768, 1280, 1920, 2560 -- se omite cualquier ancho > original
(no se inventa resolucion que la foto no tiene).

ADEMAS del escalon estandar se emite el ANCHO NATIVO del master cuando no
coincide con ninguno. Motivo: 144 de los 156 masters del catalogo miden 1600 px,
asi que la escalera se les cortaba en 1280 y en una pantalla grande o retina la
foto se veia blanda pudiendo no verse asi. Con el nativo, cada imagen ofrece
todo lo que tiene y ni un pixel inventado.

El fichero de anchos disponibles por imagen lo escribe export_api.py leyendo
este mismo directorio; el srcset del navegador se construye con esa lista y no
con una tabla fija, que era justo el fallo: se anunciaban 1920 y 2560 para
masters de 1600 y el navegador pedia ficheros que nunca existieron."""
import os, sys, glob
from PIL import Image

WIDTHS = [480, 768, 1280, 1920, 2560]
SRC_DIR = "assets/img/xaru/catalog"
OUT_DIR = "assets/img/xaru/catalog/r"

def derive(path, force=False):
    base = os.path.splitext(os.path.basename(path))[0]
    im = Image.open(path).convert("RGB")
    W, H = im.size
    made = []
    widths = [w for w in WIDTHS if w <= W]
    if W not in widths:
        widths.append(W)          # el ancho nativo, sin reescalar
    for w in widths:
        h = round(H * w / W)
        rs = im.resize((w, h), Image.LANCZOS) if w != W else im
        for ext, kw in (("avif", dict(quality=60)),
                        ("webp", dict(quality=76, method=6)),
                        ("jpg",  dict(quality=82, optimize=True, progressive=True))):
            out = f"{OUT_DIR}/{base}-{w}.{ext}"
            if os.path.exists(out) and not force:
                continue
            rs.save(out, **kw)
            made.append(out)
    return made

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    force = "--force" in sys.argv
    srcs = sorted(glob.glob(f"{SRC_DIR}/*.jpg"))
    total = 0
    for p in srcs:
        n = len(derive(p, force))
        total += n
    print(f"{len(srcs)} masters -> {total} derivadas nuevas")
