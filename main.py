import numpy as np
from matplotlib import cm, widgets as wd, pyplot as plt

# Parameters
A = 10
L = 300
n_x = 2
n_y = 1
omega = 0

# Sensitivity
choice_step = input("Whole integers? [y/n]: ")
# choice_fs = input("Fullscreen? [y/n]: ")

step = 1 if choice_step == 'y' else 0.05
fullscreen = True
#fullscreen = True if choice_fs == 'y' else False

def draw_chladni(x, y, n_x, n_y, f):
    g = (np.cos(n_x*np.pi*x/L)*np.cos(n_y*np.pi*y/L))+(np.cos(n_y*np.pi*x/L)*np.cos(n_x*np.pi*y/L))
    psi = A*g*np.cos(2*np.pi*f)
    return psi

fx = np.arange(-L, L)
fy = np.arange(-L, L)
[X,Y] = np.meshgrid(fx, fy)

Z = draw_chladni(X, Y, n_x, n_y, 1)
Z_2 = np.isclose(Z, 0, atol=1)

if not fullscreen:
    fig, axs = plt.subplots(2,2)
    axs[1, 1].contourf(X, Y, Z_2, 1,colors=['#222222','white'])
    axs[0, 1].plot(fx, draw_chladni(fx,0,n_x,n_y,1))
    axs[0, 0].plot(fy, draw_chladni(0,fy,n_x,n_y,1))
    x_ax = plt.axes([0.2, 0.30, 0.6, 0.03])
    y_ax = plt.axes([0.2, 0.25, 0.6, 0.03])
else:
    plt.contourf(X,Y,Z_2,1,colors=['#222222','white'])
    chladni = plt.gca()
    x_ax = plt.axes([0.3, 0.06, 0.4, 0.01])
    y_ax = plt.axes([0.3, 0.04, 0.4, 0.01])
    z_ax = plt.axes([0.3, 0.02, 0.4, 0.01])
    f_ax = plt.axes([0.3, 0.0, 0.4, 0.01])

#### Sliders ####
n_x = wd.Slider(x_ax, 'n_x', 0, 20, n_x, valstep=step)
n_y = wd.Slider(y_ax, 'n_y', 0, 20, n_y, valstep=step)
ATOL = wd.Slider(z_ax, 'ATOL', 0, 5, 1, valstep=0.01)
freq = wd.Slider(f_ax, 'Frequency [Hz]', 0, 10000, 1, valstep=1)

#### Update plot ####
def update(val):
    Z = draw_chladni(X, Y, n_x.val, n_y.val, freq.val)
    Z_2 = np.isclose(Z, 0, atol=ATOL.val)

    if not fullscreen:
        axs[1, 1].clear()
        axs[0, 1].clear()
        axs[0, 0].clear()
        axs[1, 1].contourf(X, Y, Z_2, 1,colors=['#222222','white'])
        axs[0, 1].plot(fx, draw_chladni(fx,0,n_x.val,n_y.val,freq.val))
        axs[0, 0].plot(fy, draw_chladni(0,fy,n_x.val,n_y.val,freq.val))
    else:
        chladni.clear()
        chladni.contourf(X,Y,Z_2,1,colors=['#222222','white'])

    print('n_x/n_y =', n_x.val/n_y.val)
    plt.draw()

n_x.on_changed(update)
n_y.on_changed(update)
ATOL.on_changed(update)
freq.on_changed(update)

plt.show()
