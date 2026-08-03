# -*- coding: utf-8 -*-
"""Logo PLANO en el beige del render. Version definitiva.

Josep lo pidio claro: plano, no en relieve, conservando el color beige y la
estructura. El relieve estaba iluminado para pared oscura y a 42 px sobre una
cabecera crema se veia sucio; eso ya esta revertido.

DE DONDE SALE CADA COSA
-----------------------
La forma es el VECTORIAL DE MARCA, que ya es plano y es la estructura buena. El
color se lleva al beige del render:

    oro plano del master   #AC8D60
    beige del render       #CFAE83

El degradado vertical del master no se reinventa: se traslada al rango del
beige con una transformacion lineal por canal, y se comprime la ganancia al 60%
porque replicar en plano toda la dispersion de un metal fotografiado exagera el
degradado y aparece bandeado.

EL BLOQUE HORIZONTAL
--------------------
El kit solo trae el vertical. El horizontal se compone con las piezas oficiales
usando las proporciones medidas en el render de Josep: XARU mide el 61,0% del
alto del simbolo, el aire entre ambos es el 29,1% de ese alto, y el simbolo baja
un 6,4% respecto a la base de XARU.

POR QUE ALFA PREMULTIPLICADO
----------------------------
Primera version: los bordes del bloque horizontal salieron con una media de
#726048, casi negro, y algun pixel reventado a #FFEEB8. Causa: al recolorear se
toco tambien el RGB de los pixeles TRANSPARENTES, que no significa nada, y al
reescalar el remuestreo mezclo ese color muerto con el del borde. Se ve como una
linea sucia alrededor de cada letra.

La cura es no dejar que un pixel transparente aporte color: se multiplica el RGB
por su alfa antes de remuestrear, se remuestrea, y se divide despues. Asi el
borde solo hereda color de lo que era visible.
"""
import cv2
import numpy as np
from PIL import Image

import os

# Rutas relativas al repositorio: los masters de marca viven ahora en brand/
# y las piezas generadas van a assets/img/xaru/. La referencia en relieve que
# origino las proporciones no se versiona —es un render de trabajo—; sus
# medidas quedan escritas como constantes mas abajo, que es lo que importa.
RAIZ = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(RAIZ, 'brand') + os.sep
OUT = os.path.join(RAIZ, 'assets', 'img', 'xaru') + os.sep
RENDER = os.environ.get('XARU_RENDER_REF', '')

# Medidas leidas del render de Josep (bloque horizontal)
XARU_REL, AIRE_REL, BAJADA_REL = 0.610, 0.291, 0.064
XARU_FRAC = 470 / 813.0          # que parte del wordmark oficial ocupa "XARU"


def beige_objetivo():
    r = np.asarray(Image.open(RENDER).convert('RGB')).astype(np.int16)[:1780]
    m = (r.max(axis=2) > 170) & ((r[..., 0] - r[..., 2]) > 55)
    px = r[m].astype(np.float64)
    return px.mean(axis=0), px.std(axis=0)


def rebeige(path):
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im).astype(np.float64)
    rgb, alfa = a[..., :3].copy(), a[..., 3]
    op = alfa > 200
    mu_o, sd_o = rgb[op].mean(axis=0), rgb[op].std(axis=0)
    mu_n, sd_n = beige_objetivo()
    k = 1.0 + (np.where(sd_o > 1, sd_n / np.maximum(sd_o, 1e-6), 1.0) - 1.0) * 0.6
    rgb = np.clip(mu_n + (rgb - mu_o) * k, 0, 255)
    # El pixel invisible no opina: se le pone el beige medio para que, si alguna
    # operacion posterior lo tocase, no aporte un color muerto.
    rgb[alfa < 1] = mu_n
    return Image.fromarray(np.dstack([rgb, alfa]).astype(np.uint8), 'RGBA')


def escalar(im, w, h):
    """Remuestreo con alfa premultiplicado, EN COMA FLOTANTE.

    Premultiplicar evita que un pixel transparente aporte color al borde. Pero
    la primera version premultiplicaba en enteros de 8 bits y eso arruinaba
    justo los pixeles que queria proteger: en un borde con alfa 10/255, el valor
    premultiplicado cae a 7, y al dividir despues por ese alfa minusculo el error
    de cuantizacion se multiplica por veinticinco. El borde salia con una media
    de #F9EECF —casi blanco— sobre un cuerpo de #B09163: un halo claro alrededor
    de cada letra. En coma flotante no hay nada que redondear hasta el final.
    """
    a = np.asarray(im).astype(np.float64)
    al = a[..., 3:4] / 255.0
    pm = cv2.resize(np.dstack([a[..., :3] * al, a[..., 3]]), (w, h),
                    interpolation=cv2.INTER_AREA if w < im.width else cv2.INTER_LANCZOS4)
    al2 = np.maximum(pm[..., 3:4] / 255.0, 1e-6)
    rgb = np.clip(pm[..., :3] / al2, 0, 255)
    alfa = np.clip(pm[..., 3], 0, 255)
    return Image.fromarray(np.dstack([rgb, alfa]).round().astype(np.uint8), 'RGBA')


def recorta(im):
    return im.crop(im.getchannel('A').getbbox())


def horizontal(H=1400):
    sim = recorta(rebeige(BRAND + 'XARU_monogram_gold.png'))
    txt = recorta(rebeige(BRAND + 'XARU_wordmark_gold.png'))
    esc = (H * XARU_REL) / (txt.height * XARU_FRAC)
    txt = escalar(txt, round(txt.width * esc), round(txt.height * esc))
    sim = escalar(sim, round(sim.width * H / sim.height), H)
    aire = round(H * AIRE_REL)
    y_sim = round(txt.height * XARU_FRAC + H * BAJADA_REL) - H
    y_txt = 0
    top = min(y_sim, y_txt)
    y_sim -= top
    y_txt -= top
    lienzo = Image.new('RGBA', (sim.width + aire + txt.width,
                                max(y_sim + sim.height, y_txt + txt.height)), (0, 0, 0, 0))
    lienzo.paste(sim, (0, y_sim), sim)
    lienzo.paste(txt, (sim.width + aire, y_txt), txt)
    return recorta(lienzo)


def main():
    horizontal().save(OUT + 'XARU_HOME_lockup_h_beige.png')
    for src, dst in (('XARU_HOME_lockup_gold.png', 'XARU_HOME_lockup_beige.png'),
                     ('XARU_wordmark_gold.png', 'XARU_wordmark_beige.png'),
                     ('XARU_monogram_gold.png', 'XARU_monogram_beige.png')):
        recorta(rebeige(BRAND + src)).save(OUT + dst)
    for f in ('XARU_HOME_lockup_h_beige.png', 'XARU_HOME_lockup_beige.png',
              'XARU_wordmark_beige.png', 'XARU_monogram_beige.png'):
        im = Image.open(OUT + f).convert('RGBA')
        a = np.asarray(im)
        op, borde = a[..., 3] > 200, (a[..., 3] > 10) & (a[..., 3] < 200)
        q, qb = a[..., :3][op], a[..., :3][borde]
        print('%-32s %-12s cuerpo #%02X%02X%02X  borde #%02X%02X%02X' % (
            f, '%dx%d' % im.size, *q.mean(axis=0).round(0).astype(int),
            *(qb.mean(axis=0).round(0).astype(int) if len(qb) else (0, 0, 0))))


if __name__ == '__main__':
    main()
