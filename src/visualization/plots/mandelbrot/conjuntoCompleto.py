'''
Conjunto de Mandelbrot.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.cm as cm
from pathlib import Path


def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n


def plot_mandelbrot():
    width, height = 1000, 1000
    max_iter = 100

    # Rango del plano complejo a visualizar
    re_start, re_end = -2.0, 1.0
    im_start, im_end = -1.5, 1.5

    # Crear una matriz de números complejos
    real = np.linspace(re_start, re_end, width)
    imag = np.linspace(im_start, im_end, height)

    mandelbrot_set = np.empty((width, height))

    for i in range(width):
        for j in range(height):
            c = complex(real[i], imag[j])
            mandelbrot_set[i, j] = mandelbrot(c, max_iter)

    # Colores
    red_gradient = plt.get_cmap('Reds', max_iter - 1)
    colors = [red_gradient(i) for i in range(red_gradient.N)]
    colors.append((0, 0, 0, 1)) 
    cmap_reds_black = ListedColormap(colors)

    # Creación de la figura
    fig = plt.figure(figsize=(10, 10), dpi=300)
    ax = plt.gca()

    ax.imshow(mandelbrot_set.T, cmap=cmap_reds_black, origin='lower',
              extent=[re_start, re_end, im_start, im_end])
    ax.set_xticks([])
    ax.set_yticks([])

    plt.tight_layout(pad=0.1)

    return fig


if __name__ == "__main__":
    fig = plot_mandelbrot()
    
    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"mandelbrot.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()