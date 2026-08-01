#!/usr/bin/env python3
"""Genera derivadas responsive (AVIF/WebP/JPEG) para el catalogo XARU HOME.
Anchos: 480, 768, 1280, 1920, 2560 -- se omite cualquier ancho > original
(no se inventa resolucion que la foto no tiene)."""
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
    for w in WIDTHS:
        if w > W:
            continue
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
