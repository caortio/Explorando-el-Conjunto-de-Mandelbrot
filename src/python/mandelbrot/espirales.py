"""
Conjunto de Mandelbrot completo con espiral para c = -0.43 + 0.47i.
NOTA: si se desea ver la espiral para otro valor de c, basta modificar este en la línea 45.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pathlib import Path


def mandelbrot_escape_time(c, max_iter=500):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n


def plot_mandelbrot_espiral_5():
    width, height = 1000, 1000
    max_iter = 500

    re_start, re_end = -2.0, 1.0
    im_start, im_end = -1.5, 1.5

    # Colormap
    red_gradient = plt.get_cmap('Reds', max_iter - 1)
    colors = [red_gradient(i) for i in range(red_gradient.N)]
    colors.append((0, 0, 0, 1)) 
    cmap_reds_black = ListedColormap(colors)

    # Matriz del conjunto
    real = np.linspace(re_start, re_end, width)
    imag = np.linspace(im_start, im_end, height)
    mandelbrot_set = np.empty((width, height))

    for i in range(width):
        for j in range(height):
            c = complex(real[i], imag[j])
            mandelbrot_set[i, j] = mandelbrot_escape_time(c, max_iter)

    # Órbita para c concreto 
    c_espiral = -0.43 + 0.47j
    z = 0 + 0j
    orbit = []
    for _ in range(100):
        z = z**2 + c_espiral
        orbit.append(z)
    orbit = np.array(orbit)

    fig = plt.figure(figsize=(10, 10), dpi=300)

    plt.imshow(mandelbrot_set.T, cmap=cmap_reds_black, origin='lower',
        extent=[re_start, re_end, im_start, im_end])

    # Espiral
    plt.plot(orbit.real, orbit.imag, color='blue', linewidth=1.5)
    plt.scatter([c_espiral.real], [c_espiral.imag], color='blue', s=60, zorder=10)

    plt.xticks([])
    plt.yticks([])

    plt.tight_layout(pad=0.2)
    return fig


if __name__ == "__main__":
    fig = plot_mandelbrot_espiral_5()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"espiral.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()