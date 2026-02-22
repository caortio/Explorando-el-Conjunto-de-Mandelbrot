"""
Panel comparativo del Conjunto de Mandelbrot y varios conjuntos de Julia llenos  
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.cm as cm
from matplotlib.patches import ConnectionPatch
from pathlib import Path


def mandelbrot_escape(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n


def generate_julia_set(c_val, max_iter, width, height, x_start, x_end, y_start, y_end):
    real = np.linspace(x_start, x_end, width)
    imag = np.linspace(y_start, y_end, height)
    julia_data = np.empty((width, height))

    for i in range(width):
        for j in range(height):
            z = complex(real[i], imag[j])
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z*z + c_val
                n += 1
            julia_data[i, j] = n

    return julia_data


def plot_mandelbrot_julia_panel():
    # ── Parámetros globales ────────────────────────────────────────
    mandel_width, mandel_height = 1000, 1000
    mandel_max_iter = 1024
    mandel_re_start, mandel_re_end = -2.0, 1.0
    mandel_im_start, mandel_im_end = -1.5, 1.5

    julia_width, julia_height = 300, 300
    julia_max_iter = 1024
    julia_x_start, julia_x_end = -1.5, 1.5
    julia_y_start, julia_y_end = -1.5, 1.5

    # Valores de c para los 6 conjuntos de Julia
    julia_c_values = [
        -0.781+0.14j,       # Doble-espiral
        -0.12 + 0.75j,      # Conejo
        -0.76+0.09j,        # Caballo de mar
        0.255,              # Cerebro
        0.4 +0.3j,          #valor fuera de Mandelbrot
        0.28+0.008j         # Elefante
    ]

    # ── Colormap Mandelbrot: blanco fondo + negro interior ────────
    colors = [(1, 1, 1, 1)] * mandel_max_iter
    colors.append((0, 0, 0, 1))
    cmap_white_black = ListedColormap(colors)

    # ── Cálculo Mandelbrot ─────────────────────────────────────────
    real = np.linspace(mandel_re_start, mandel_re_end, mandel_width)
    imag = np.linspace(mandel_im_start, mandel_im_end, mandel_height)
    mandelbrot_set = np.empty((mandel_width, mandel_height))

    for i in range(mandel_width):
        for j in range(mandel_height):
            c = complex(real[i], imag[j])
            mandelbrot_set[i, j] = mandelbrot_escape(c, mandel_max_iter)

    # ── Cálculo de los 6 conjuntos de Julia ────────────────────────
    julia_sets_data = []
    for c_val in julia_c_values:
        data = generate_julia_set(
            c_val, julia_max_iter, julia_width, julia_height,
            julia_x_start, julia_x_end, julia_y_start, julia_y_end
        )
        julia_sets_data.append(data)

    # ── Figura y GridSpec ──────────────────────────────────────────
    fig = plt.figure(figsize=(8.27, 11.68), dpi=300)  
    gs = plt.GridSpec(3, 3, wspace=0.1, hspace=0.1)

    # Mandelbrot central
    ax_mandel = fig.add_subplot(gs[1, 1])
    ax_mandel.imshow(
        mandelbrot_set.T, cmap=cmap_white_black, origin='lower',
        extent=[mandel_re_start, mandel_re_end, mandel_im_start, mandel_im_end]
    )
    ax_mandel.set_xticks([])
    ax_mandel.set_yticks([])

    # Posiciones de los Julias
    julia_positions = [
        gs[0, 0], gs[0, 2],    # arriba izq, arriba der
        gs[1, 0], gs[1, 2],    # medio izq, medio der
        gs[2, 0], gs[2, 2]     # abajo izq, abajo der
    ]

    ax_julias = [fig.add_subplot(pos) for pos in julia_positions]

    # Dibujar cada Julia + título con valor de c
    for i, (data, c_val, ax) in enumerate(zip(julia_sets_data, julia_c_values, ax_julias)):
        ax.imshow(
            data.T, cmap='inferno', origin='lower',
            extent=[julia_x_start, julia_x_end, julia_y_start, julia_y_end]
        )
        ax.set_title(rf"$c = {c_val.real:.3f} {c_val.imag:+.3f}i$", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])

    # Flechas de conexión Mandelbrot → cada Julia
    for c_val, ax_julia in zip(julia_c_values, ax_julias):
        xyA = (c_val.real, c_val.imag)          
        xyB = (0, 0)                            
        con = ConnectionPatch(
            xyA=xyA, xyB=xyB,
            coordsA="data", coordsB="data",
            axesA=ax_mandel, axesB=ax_julia,
            arrowstyle="->", color='blue',
            linewidth=1.5, linestyle='-', alpha=0.8,
            shrinkB=5
        )
        fig.add_artist(con)

    plt.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.03)
    return fig

if __name__ == "__main__":
    fig = plot_mandelbrot_julia_panel()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"panelMandelbrotJulia.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()