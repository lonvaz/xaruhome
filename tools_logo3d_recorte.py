# -*- coding: utf-8 -*-
"""Recorte del logo 3D de XARU HOME sobre fondo transparente.

QUE SE CONSERVA Y QUE SE QUITA
------------------------------
Se conserva todo el pixel del metal: forma, color, bisel, brillo y las caras en
sombra que dan el relieve. No se recolorea, no se aplana, no se reescala de
forma no uniforme. Lo unico que se decide es que pixel es logo y cual es pared.

Se quita la pared y con ella la sombra proyectada, que esta pintada sobre la
pared y no sobre el metal: arrastrarla dejaria una mancha oscura flotando en
cuanto el logo cayera sobre fondo claro. El relieve no depende de ella, vive en
el propio biselado.

LO QUE COSTO, Y POR QUE ACABA ASI
---------------------------------
Detras del arco la pared tiene un punto de luz dorada que iguala al metal en
brillo y en calidez —medido: pared iluminada V 139 calidez 48; vertice del arco
V 149 calidez 45—. Ningun umbral de color los separa, y se probaron unos
cuantos. Tambien se descarto usar el vectorial de marca como silueta: el render
tiene letras propias y el solape con el master se queda entre 0,60 y 0,86, de
modo que imponerlo cambiaria la forma que hay que respetar.

Lo que si funciona son tres cosas juntas:

1. CARAS BRILLANTES. La cara que mira a la luz es mas clara que cualquier punto
   de pared, y forma trazos continuos y cerrados: da la topologia correcta.
   El texto pequeño necesita un listón mas bajo que el simbolo —"HOME" apenas
   pasa de V 188 en su percentil 95 y con el umbral alto se partia la H—, y
   puede permitirselo porque el resplandor esta arriba, alrededor del arco, no
   sobre el texto.

2. CONTRAFORMAS. El interior del arco y los ojos de la A, la R y la O salen como
   huecos de esa estructura. Son fondo por definicion, por iluminados que esten,
   y sembrarlos asi es lo que echa el resplandor de dentro del arco.

3. CRECIMIENTO CON UMBRAL LOCAL. Desde las caras brillantes se crece hacia el
   bisel —medido en un corte transversal del propio render: la pared pasa de
   V~15 a V~190 en seis a nueve pixeles— aceptando solo pixeles que destacan
   sobre SU fondo local, no sobre un valor fijo. El fondo local se obtiene por
   apertura morfologica con un radio mayor que el grosor del trazo, asi que el
   resplandor, que es suave y ancho, queda dentro del fondo y deja de contar.
"""
import numpy as np
import cv2
from PIL import Image
from scipy import ndimage as ndi

SRC = '/root/.claude/uploads/75132e92-c788-52fb-8fe7-d53929193804/53e5506d-logo_xau.png'
OUT = '/home/claude/work/logo3d/'
BISEL = 9        # ancho medido de la faja biselada, en px del render
RADIO_FONDO = 60  # mayor que el grosor del trazo, para que el trazo no entre en el fondo


def _caras(rgb, vmin, cmin, minimo):
    R, B = rgb[..., 0].astype(np.int16), rgb[..., 2].astype(np.int16)
    V = rgb.max(axis=2)
    m = (V > vmin) & ((R - B) > cmin)
    m = ndi.binary_closing(m, np.ones((7, 7)))
    lbl, n = ndi.label(m)
    if n:
        sizes = ndi.sum(m, lbl, range(1, n + 1))
        m = np.isin(lbl, 1 + np.nonzero(sizes > minimo)[0])
    return m


def caras_brillantes(rgb):
    """Umbral alto en general; mas bajo donde vive el texto pequeño."""
    alto = _caras(rgb, 185, 52, 300)
    bajo = _caras(rgb, 150, 44, 150)
    # El simbolo es el componente mas alto: por debajo de el empieza el texto,
    # y ahi no llega el resplandor del arco.
    lbl, n = ndi.label(alto)
    if n:
        objs = ndi.find_objects(lbl)
        i = max(range(n), key=lambda j: objs[j][0].stop - objs[j][0].start)
        limite = objs[i][0].stop
        banda = np.zeros_like(alto)
        banda[limite:] = True
        # En el bloque horizontal el texto va al lado, no debajo: se añade
        # tambien lo que quede a la derecha del simbolo.
        banda[:, objs[i][1].stop:] = True
        return alto | (bajo & banda)
    return alto


def contraformas(br):
    """Huecos encerrados por los trazos. Fondo por definicion."""
    return ndi.binary_fill_holes(br) & ~br


def fondo_local(rgb):
    """Nivel de la pared bajo cada pixel, resplandor incluido."""
    V = rgb.max(axis=2).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * RADIO_FONDO + 1,) * 2)
    return cv2.morphologyEx(V, cv2.MORPH_TOPHAT, k).astype(np.int16)


def recortar(rgb, realce=20):
    br = caras_brillantes(rgb)
    dentro = contraformas(br)
    faja = ndi.binary_dilation(br, np.ones((BISEL * 2 + 1,) * 2))
    solido = br | (faja & (fondo_local(rgb) > realce))
    solido &= ~ndi.binary_erosion(dentro, np.ones((5, 5)))

    solido = ndi.binary_closing(solido, np.ones((5, 5)))
    lbl, n = ndi.label(solido)
    if n:
        sizes = ndi.sum(solido, lbl, range(1, n + 1))
        solido = np.isin(lbl, 1 + np.nonzero(sizes > 300)[0])
    # Poros de la textura cepillada; no son agujeros de la marca.
    huecos = ndi.binary_fill_holes(solido) & ~solido
    lbl, n = ndi.label(huecos)
    if n:
        sizes = ndi.sum(huecos, lbl, range(1, n + 1))
        solido |= np.isin(lbl, 1 + np.nonzero(sizes < 300)[0])
    return solido


def alfa_limpia(solido):
    """Un pixel de erosion antes de suavizar: el borde exacto es mezcla de oro y
    pared, y cortando ahi se lee como una linea sucia sobre fondo claro."""
    a = ndi.binary_erosion(solido, np.ones((3, 3))).astype(np.float32)
    return np.clip(cv2.GaussianBlur(a, (0, 0), 0.8), 0, 1)


def main():
    a = np.asarray(Image.open(SRC).convert('RGB'))
    for nom, rgb in (('vertical', a[:1780]), ('horizontal', a[1792:])):
        rgb = np.ascontiguousarray(rgb)
        im = Image.fromarray(
            np.dstack([rgb, (alfa_limpia(recortar(rgb)) * 255).round().astype(np.uint8)]), 'RGBA')
        im = im.crop(im.getchannel('A').getbbox())
        im.save(OUT + 'xaru_3d_%s.png' % nom)
        print('%-11s %s  transparente %.1f%%' % (
            nom, im.size, 100 * (np.asarray(im.getchannel('A')) == 0).mean()))


if __name__ == '__main__':
    main()
