"""
Conjunto de Julia para el valor c=-0.123+0.745i
NOTA: si se desea ver la espiral para otro valor de c, basta modificar este en la línea 35.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


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


def plot_julia_relacion_mandelbrot():
    width, height = 300, 300
    max_iter = 750
    x_start, x_end = -1.5, 1.5
    y_start, y_end = -1.5, 1.5

    c_value =-0.123+0.745j

    julia_matrix = generate_julia_set(c_value, max_iter, width, height, 
                                      x_start, x_end, y_start, y_end)

    fig = plt.figure(figsize=(7, 7), dpi=300)

    plt.imshow(julia_matrix.T, cmap='hot', origin='lower',
        extent=[x_start, x_end, y_start, y_end])

    plt.xticks([])
    plt.yticks([])

    plt.tight_layout(pad=0.3)

    return fig


if __name__ == "__main__":
    fig = plot_julia_relacion_mandelbrot()

    import os 
    from pathlib import Path
    ruta_completa = Path("resultados/figuras") / f"juliaValorC.pdf"

    fig.savefig(ruta_completa, format="pdf", dpi=400, bbox_inches="tight")
    print(f"Figura guardada en: {ruta_completa.resolve()}")
    plt.show()