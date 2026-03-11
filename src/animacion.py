import numpy as np
import matplotlib.pyplot as plt

max_iter = 80
N = 400

# Mandelbrot grid
x = np.linspace(-2,1,N)
y = np.linspace(-1.5,1.5,N)
X,Y = np.meshgrid(x,y)
C = X + 1j*Y

# Julia grid
xj = np.linspace(-2,2,N)
yj = np.linspace(-2,2,N)
XJ,YJ = np.meshgrid(xj,yj)
Z0 = XJ + 1j*YJ


def mandelbrot():
    Z = np.zeros_like(C)
    M = np.zeros(C.shape)

    for i in range(max_iter):
        Z = Z**2 + C
        mask = np.abs(Z) < 2
        M += mask

    return M


def julia(c):
    Z = Z0.copy()
    M = np.zeros(Z.shape)

    for i in range(max_iter):
        Z = Z**2 + c
        mask = np.abs(Z) < 2
        M += mask

    return M


M = mandelbrot()
c = -0.4 + 0.6j
J = julia(c)

fig,(ax1,ax2) = plt.subplots(1,2)

img1 = ax1.imshow(M,extent=(-2,1,-1.5,1.5))
ax1.set_title("Mandelbrot")

img2 = ax2.imshow(J,extent=(-2,2,-2,2))
ax2.set_title("Julia")

def onclick(event):
    if event.inaxes == ax1:
        c = event.xdata + 1j*event.ydata
        J = julia(c)
        img2.set_data(J)
        # Convertimos c a formato con 'i' en lugar de 'j'
        c_str = f"{c.real:.2f} {'+' if c.imag >= 0 else '-'} {abs(c.imag):.2f}i"
        ax2.set_title(f"Julia  c={c_str}")
        fig.canvas.draw()

fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()