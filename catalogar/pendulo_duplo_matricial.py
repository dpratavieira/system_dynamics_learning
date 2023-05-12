import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


l1 = .25
l2 = .25
m1 = 10
m2 = m1/3
c1, c2 = .1, .1

g = 9.81

def alpha1(th1,th2):
    return (l2/l1)*(m2/(m1+m2))*np.cos(th1-th2)

def alpha2(th1,th2):
    return (l1/l2)*np.cos(th1-th2)

def f1(th1,th2,w1,w2):
    return -(l2/l1)*(m2/(m1+m2))*(w2**2)*np.sin(th1-th2) - (g/l1)*np.sin(th1) - c1*w1 - c2*(w1 - w2)

def f2(th1,th2,w1,w2):
    return -(l1/l2)*(w1**2)*np.sin(th1-th2) - (g/l2)*np.sin(th2) - c2*(w2 - w1)

def g1(th1,th2,w1,w2):
    return (f1(th1,th2,w1,w2) - alpha1(th1,th2) * f2(th1,th2,w1,w2)) / (1 - alpha1(th1,th2)*alpha2(th1,th2))

def g2(th1,th2,w1,w2):
    return (f2(th1,th2,w1,w2) - alpha2(th1,th2) * f1(th1,th2,w1,w2)) / (1 - alpha1(th1,th2)*alpha2(th1,th2))

def modelo(t,z):
    return [z[2], z[3], g1(z[0], z[1], z[2], z[3]), g2(z[0], z[1], z[2], z[3])]

a1 = np.arange(10, 15, 1)
a2 = np.arange(10, 15, 1)
v1 = 0*a1
v2 = 0*a1

z0_iter = np.array([a1, a2, v1, v2]).T

cont=1
for z0i in z0_iter:
    z0 = np.deg2rad(np.array(z0i))
    t_inicial = 0
    t_final = 30
    N_pts = 100*(t_final - t_inicial)
    t = np.linspace(t_inicial, t_final, N_pts)

    th = solve_ivp(modelo, (t_inicial, t_final), z0, t_eval=t, max_step=5e-3)
    th1  = th.y[0,:]
    th2  = th.y[1,:]
    th1p = th.y[2,:]
    th2p = th.y[3,:]
    

    x1 = l1*np.sin(th1)
    y1 = -l1*np.cos(th1)
    x2 = x1 + l2*np.sin(th2)
    y2 = y1 - l2*np.cos(th2)

    fig = plt.figure(figsize=(15, 5), constrained_layout=True)
    plt.subplot(131)
    plt.plot(x1,y1)
    plt.plot(x2,y2)
    plt.title('Traço X vs Y')
    plt.xlabel('tempo [s]')
    plt.ylabel('Ângulo vertical [graus]')
    plt.grid('on')



    plt.subplot(132)
    plt.plot(th.t, np.rad2deg(th1))
    plt.plot(th.t, np.rad2deg(th2))
    plt.xlabel('tempo [s]')
    plt.ylabel('ângulo [graus]')
    plt.title('Série Temporal da posição')
    plt.grid('on')

    plt.subplot(133)
    plt.plot(th1p, np.rad2deg(th1))
    plt.plot(th2p, np.rad2deg(th2))
    plt.xlabel('ângulo [graus]')
    plt.ylabel('vel. angular [rad/s]')
    plt.title('Diagrama de fase')
    plt.grid('on')

    texto = "Figure {:d} - Th_1 = {:d}° | Th_2 = {:d}° ".format(cont, z0i[0],z0i[1])

    plt.suptitle(texto)

plt.show()