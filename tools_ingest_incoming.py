#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recoge las imágenes que caen en XARU_HOME/incoming y las integra al catálogo.

Pensado para el trabajo en paralelo: Josep (o quien le ayude) deja los ficheros
con el NOMBRE EXACTO del slot, y esto los valida, los normaliza a 1600 px y los
deja listos. No toca nada que no cuadre: si un fichero no corresponde a un slot
real del catálogo, lo dice y lo deja donde está.

Uso:
    python3 tools_ingest_incoming.py /ruta/a/incoming
"""
import os, re, sys, shutil
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import catalog_spec as S

DEST = "assets/img/xaru/catalog"
MIN_W = 1200          # por debajo de esto no da la talla ni reescalando
TARGET_W = 1600

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def valid_slots():
    out = set()
    for grp, pre in ((S.RESIDENTIAL, "pr"), (S.HOSPITALITY, "ch"), (S.LAND, "ld")):
        for cat, items in grp.items():
            for it in items:
                out.add(f"{pre}-{slug(cat)}-{slug(it[0])}")
    return out

def main(src):
    slots = valid_slots()
    have = {f[:-4] for f in os.listdir(DEST) if f.endswith(".jpg")}
    ok = skipped = bad = 0
    for fn in sorted(os.listdir(src)):
        if fn.startswith("."):
            continue
        stem, ext = os.path.splitext(fn)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        if stem not in slots:
            print(f"  NOMBRE NO VÁLIDO  {fn}  (no corresponde a ningún slot)")
            bad += 1
            continue
        if stem in have:
            print(f"  ya existía, omito   {stem}")
            skipped += 1
            continue
        p = os.path.join(src, fn)
        try:
            im = Image.open(p); im.load(); im = im.convert("RGB")
        except Exception as e:
            print(f"  NO ES IMAGEN       {fn}: {e}")
            bad += 1
            continue
        w, h = im.size
        if w < MIN_W:
            print(f"  DEMASIADO PEQUEÑA  {fn}: {w}x{h} (mínimo {MIN_W} de ancho)")
            bad += 1
            continue
        if h > w:
            print(f"  VERTICAL, rechazo  {fn}: {w}x{h} (se pidió horizontal)")
            bad += 1
            continue
        im.resize((TARGET_W, round(h * TARGET_W / w)), Image.LANCZOS).save(
            os.path.join(DEST, stem + ".jpg"),
            quality=86, optimize=True, progressive=True)
        print(f"  integrada          {stem}  <- {w}x{h}")
        ok += 1
    print(f"\n{ok} integradas · {skipped} ya estaban · {bad} rechazadas")
    if ok:
        print("Ahora: python3 tools_derivatives.py  y commit.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else
         "/mnt/user-data/uploads/XARU_HOME/incoming")
