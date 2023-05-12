import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc


g=9.8
m1=10
m2=3
l1=.25
l2=.25

def f1(w1, w2, theta_01, theta_02):
    dw1dt = (-g * (2 * m1 + m2) * np.sin(theta_01) - m2 * g * np.sin(theta_01 - 2 * theta_02) - 2 * np.sin(theta_01 - theta_02) * m2 *(w2 * w2 * l2 + w1 * w1 * l1 * np.cos(theta_01 - theta_02) ) ) / (l1 * (2 * m1 + m2 - m2 * np.cos(2*theta_01 - 2*theta_02) ) )
    return dw1dt

def f2(w1, w2, theta_01, theta_02):
    dw2dt = ( 2 * np.sin(theta_01-theta_02) * (w1*w1*l1*(m1+m2) + g*(m1+m2)*np.cos(theta_01) + w2*w2*l2*m2*np.cos(theta_01-theta_02) ) ) / (l2 * (2*m1 + m2 - m2*np.cos(2*theta_01-2*theta_02) ) )
    return dw2dt

def f3(w1, w2, theta_01, theta_02):
    return w1

def f4(w1, w2, theta_01, theta_02):
    return w2


def model(t,z):
    dw1dt  = f1(z[0], z[1], z[2], z[3])
    dw2dt  = f2(z[0], z[1], z[2], z[3])
    dth1dt = f3(z[0], z[1], z[2], z[3])
    dth2dt = f4(z[0], z[1], z[2], z[3])
    
    dzdt = [dw1dt, dw2dt, dth1dt, dth2dt]
    return dzdt


# v1 = [ 0,  0,  0,   0,  0,  0,  0,   0,  0,  0,  0,   0,   0,   0,   0]
# v2 = [ 0,  0,  0,   0,  0,  0,  0,   0,  0,  0,  0,   0,   0,   0,   0]
# a1 = [30, 30, 30,  30, 60, 60, 60,  60, 90, 90, 90,  90,  30,  60,  90]
# a2 = [30, 60, 90, 120, 30, 60, 90, 120, 30, 60, 90, 120, -30, -60, -90]

a1 = np.arange(10, 60, 1)
a2 = np.arange(10, 60, 1)
v1 = 0*a1
v2 = 0*a1




z0_iter = np.array([v1, v2, a1, a2]).T

cont=1
for z0i in z0_iter:
    z0 = np.deg2rad(np.array(z0i))
    t_inicial = 0
    t_final = 30
    N_pts = 500
    t = np.linspace(t_inicial, t_final, N_pts)

    th = solve_ivp(model, (t_inicial, t_final), z0, t_eval=t, max_step=5e-3)
    th1p = th.y[0,:]
    th2p = th.y[1,:]
    th1 = th.y[2,:]
    th2 = th.y[3,:]

    x1 = l1*np.sin(th1)
    y1 = -l1*np.cos(th1)
    x2 = x1 + l2*np.sin(th2)
    y2 = y1 - l2*np.cos(th2)

    fig = plt.figure(figsize=(15, 5), constrained_layout=True)
    plt.subplot(131)
    plt.plot(x1,y1)
    plt.plot(x2,y2)
    plt.title('Traço X vs Y')
    plt.grid('on')



    plt.subplot(132)
    plt.plot(th.t, np.rad2deg(th1))
    plt.plot(th.t, np.rad2deg(th2))
    plt.xlabel('tempo [s]')
    plt.ylabel('Ângulo vertical [graus]')
    plt.title('Série Temporal da posição')
    plt.grid('on')

    plt.subplot(133)
    plt.plot(th1p, np.rad2deg(th1))
    plt.plot(th2p, np.rad2deg(th2))
    plt.xlabel('ângulo [graus]')
    plt.ylabel('vel. angular [rad/s]')
    plt.title('Diagrama de fase')
    plt.grid('on')

    texto = "Figure {:d} - Th_1 = {:d}° | Th_2 = {:d}° ".format(cont, z0i[2],z0i[3])

    plt.suptitle(texto)

    fig.canvas.manager.set_window_title(texto)
    plt.savefig("Figure{:02d}.png".format(cont))
    cont = cont + 1

plt.show()

